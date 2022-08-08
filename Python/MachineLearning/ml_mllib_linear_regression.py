#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import findspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression
import pyspark.sql.functions  as fn
from datetime import datetime
from kafka import KafkaConsumer

global parking



def main():
    findspark.init(spark_home='/opt/spark')
    consumer = KafkaConsumer(bootstrap_servers=['hadoop-namenode'])
    parkings = list(consumer.topics())
    parser = argparse.ArgumentParser(
        description="Load Data to Hadoop with Spark Streaming")
    parser.add_argument("-p", "--parking", action="store", required=True,
                        choices=parkings, help="Parking to be executed")
    try:
        args = parser.parse_args()
    except SystemError as excep:
        print(excep)
        raise Exception("Problema con argumentos")

    global parking
    parking = args.parking

    # Spark session & context
    spark = (SparkSession
             .builder
             .master('local[*]')
             .appName('ml_'+parking+'_linear_regression')
             .getOrCreate())

    spark.sparkContext.setLogLevel("ERROR")
    sc = spark.sparkContext

    now = datetime.now()

    df_parking_machine_learning = spark \
        .read \
        .parquet(f"hdfs://hadoop-namenode:9000/machineLearning/Parkings/{parking}/year={now.year}/month={now.month - 1}/")

    df_parking_machine_learning = df_parking_machine_learning.drop("parking_id", "hour", "minutes", "day").orderBy("datetime")

    vectorAssembler = VectorAssembler(
                        inputCols = ["parking_temperature", "parking_humidity", 
                                     "area_total_spots", "parking_wind_speed",
                                     "parking_closed", "parking_holiday_status",
                                     "area_available_spots", "area_occupied_spots",
                                     "slot_state"],
                        outputCol = 'features')

    va_df_parking = vectorAssembler.transform(df_parking_machine_learning)
    va_df_parking = va_df_parking \
                        .select(['datetime', "level_id",
                                 "area_id", "slot_id",
                                 'features', 'area_occupation_percentage'])
    
    train_df, test_df = va_df_parking.randomSplit([0.7, 0.3])

    lr = LinearRegression(featuresCol = 'features', labelCol='area_occupation_percentage', maxIter=10, regParam=0.3, elasticNetParam=0.8)
    lr_model = lr.fit(train_df)
    print("Coefficients: " + str(lr_model.coefficients))
    print("Intercept: " + str(lr_model.intercept))

    trainingSummary = lr_model.summary
    print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
    print("r2: %f" % trainingSummary.r2)

    lr_predictions = lr_model.transform(test_df)

    lr_evaluator = RegressionEvaluator(predictionCol="prediction", \
                    labelCol="area_occupation_percentage",metricName="r2")
    print("R Squared (R2) on test data = %g" % lr_evaluator.evaluate(lr_predictions))

    predictions = lr_model.transform(test_df)
    predictions = predictions.select("datetime", "level_id", "area_id",
                    "slot_id","prediction","area_occupation_percentage",
                    "features") \
                .withColumnRenamed("prediction", "area_occupation_percentage_target")

    predictions = predictions \
        .dropDuplicates((['datetime','level_id', 'area_id'])) \
        .select("*") \
        .withColumn("year", fn.year(fn.col('datetime'))) \
        .withColumn("month", fn.month(fn.col('datetime'))) \
        .withColumn("day", fn.dayofmonth(fn.col('datetime'))) \
        .withColumn("hour", fn.hour(fn.col('datetime'))) \
        .withColumn("minute", fn.minute(fn.col('datetime'))) \
        .drop("features", "slot_id", 'datetime')
    
    predictions \
        .write \
        .format("parquet") \
        .mode("overwrite") \
        .partitionBy("year", "month", "day", "hour", "minute") \
        .save(f"hdfs://hadoop-namenode:9000/predictions/Parkings/{parking}/")

if __name__ == '__main__':
    main()
