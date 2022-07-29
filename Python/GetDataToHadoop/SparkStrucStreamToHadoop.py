#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import re
import findspark
from pyspark.sql.window import Window
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import logging

global parking

os.environ["HADOOP_USER_NAME"] = "hadoop"
findspark.init(spark_home='/opt/spark')


def CountOccupation(lista):
    i = 0
    for opp in lista:
        if opp == True:
            i += 1
    return i


def percentagetoString(sp_total, sp_ocupied):
    percnt = int((sp_ocupied*100)/sp_total)
    if percnt >= 0 and percnt <= 25:
        return "Empty"
    elif percnt > 25 and percnt <= 50:
        return "Almost Empty"
    elif percnt > 50 and percnt <= 75:
        return "Almost Full"
    elif percnt > 75 and percnt <= 100:
        return "Full"
    else:
        return "Other"


def func(batch_df, batch_id):

    batch_df.persist()
        # print(parking)
    try:
        df = batch_df.withColumn("value", col("value").cast("string"))
        # print(df.show())
        tableSchema = StructType() \
            .add("parking_name", StringType())\
            .add("parking_id", StringType())\
            .add("parking_address", StringType())\
            .add("parking_description", StringType())\
            .add("device_timestamp", TimestampType())\
            .add("device_id", StringType())\
            .add("parking_latitude", DoubleType())\
            .add("parking_longitude", DoubleType())\
            .add("parking_temperature", StringType())\
            .add("parking_humidity", StringType())\
            .add("parking_uuid", StringType())\
            .add("device_level_id", StringType())\
            .add("device_area_id", StringType())\
            .add("device_area_name", StringType())\
            .add("device_spots", StringType())\
            .add("device_slots", ArrayType(BooleanType()))\
            .add("parking_weather_status", StringType())\
            .add("parking_weather_status_detailed", StringType())\
            .add("parking_wind_speed", DoubleType())\
            .add("parking_holiday_status", BooleanType())\
            .add("parking_holiday_description", StringType())\
            .add("parking_holiday_type", StringType())\
            .add("parking_closed", BooleanType())

        prov = df.select("*", from_json("value",
                        tableSchema).alias("data_parsed")).select("data_parsed.*")

        dlist = prov.columns

        dfalldata = prov.select(dlist)
        df_partitioned = dfalldata.withColumn("year", year(col("device_timestamp"))) \
            .withColumn("month", month(col("device_timestamp"))) \
            .withColumn("day", dayofmonth(col("device_timestamp"))) \
            .withColumn("hour", hour(col("device_timestamp"))) \
            .withColumn("minutes", minute(col("device_timestamp"))) \

        countOcuppation = udf(lambda x: CountOccupation(x), IntegerType())
        percentageOcuppation = udf(
            lambda x, y: percentagetoString(x, y), StringType())
        areaAvailableSpots = udf(lambda x, y: x-y, IntegerType())
        percentage = udf(lambda x, y: int((y*100)/x), IntegerType())

        df_partitioned = df_partitioned\
            .withColumnRenamed("device_area_name", "area_name")\
            .withColumnRenamed("device_area_id", "area_id")\
            .withColumnRenamed("device_level_id", "level_id")\
            .withColumn("area_occupied_spots", countOcuppation(col("device_slots")))\
            .withColumn("area_occupation", percentageOcuppation(col("device_spots").cast("int"), col("area_occupied_spots").cast("int")))\
            .withColumn("area_occupation_percentage", percentage(col("device_spots").cast("int"), col("area_occupied_spots").cast("int")))\
            .withColumn("area_available_spots", areaAvailableSpots(col("device_spots").cast("int"), col("area_occupied_spots").cast("int")))\
            .withColumnRenamed("device_spots", "area_total_spots")\
            .withColumn("level_name", concat(lit("Piso "), col("level_id")))\
            .withColumn("level_id", col("level_id").cast("int"))\
            .withColumn("area_id", col("area_id").cast("int"))\
            .withColumn("area_total_spots", col("area_total_spots").cast("int"))

        df_partitioned = df_partitioned.select(
            "*", posexplode("device_slots").alias("slot_id", "slot_state"))
        df_partitioned = df_partitioned \
            .withColumn("slot_id", col("slot_id") + 1)
        #hora = 8
        # print(df_partitioned.first().show())
    
        hora = df_partitioned.first()['hour']

        if not df_partitioned.rdd.isEmpty() and hora > 7 and hora < 22:
            print("Guardando Data en Hadoop")
            df_partitioned\
                .write\
                .mode("append")\
                .format("parquet")\
                .partitionBy("year", "month", "day", "hour") \
                .save("hdfs://hadoop-namenode:9000/data/Parkings/"+parking+"/")
    except Exception as e:
        print(e)
    batch_df.unpersist()


def main():
    directory = "/opt/smart-parking/Python/GetData/Parkings"
    parkings = os.listdir(directory)
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
             .appName(parking+'HDFS')
             .config('spark.jars', 'file:///opt/smart-parking/Python/Spark-Jars-Utils/spark-sql-kafka-0-10_2.12-3.2.1.jar,file:///opt/smart-parking/Python/Spark-Jars-Utils/kafka-clients-3.1.0.jar')
             .config('spark.executor.extraClassPath', 'file:///opt/smart-parking/Python/Spark-Jars-Utils/spark-sql-kafka-0-10_2.12-3.2.1.jar:file:///opt/smart-parking/Python/Spark-Jars-Utils/kafka-clients-3.1.0.jar')
             .config('spark.executor.extraLibrary', 'file:///opt/smart-parking/Python/Spark-Jars-Utils/spark-sql-kafka-0-10_2.12-3.2.1.jar:file:///opt/smart-parking/Python/Spark-Jars-Utils/kafka-clients-3.1.0.jar')
             .config('spark.driver.extraClassPath', 'file:///opt/smart-parking/Python/Spark-Jars-Utils/spark-sql-kafka-0-10_2.12-3.2.1.jar:file:///opt/smart-parking/Python/Spark-Jars-Utils/kafka-clients-3.1.0.jar')
             .getOrCreate())

    spark.sparkContext.setLogLevel("ERROR")
    sc = spark.sparkContext

    # Subscribe to 1 topic
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "hadoop-namenode:9092") \
        .option("subscribe", parking) \
        .load()
    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    # Inicia la consulta e imprime el resultado
    CHECKPOINT_DIRECTORY = 'file:///opt/commitLogHadoop/'+parking+"/CommitLog"
    try:
        df \
            .writeStream\
            .trigger(processingTime='300 seconds')\
            .outputMode("append") \
            .option("checkpointLocation", CHECKPOINT_DIRECTORY)\
            .foreachBatch(func) \
            .start()\
            .awaitTermination()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
