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
import pyspark.sql.functions as fn
from datetime import datetime
from kafka import KafkaConsumer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

global parking


def enviar_mail(receiver_address: str, subject: str, mail_content: str,
                sender_address='smartpsystem@gmail.com',
                ):

    sender_pass = 'vtyrkfqciworubfg'

    try:
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = subject  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        # login with mail_id and password
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as excep:
        print('Exception: '+excep)
        print('Mail not sent!!. ')


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

    df_parking_machine_learning = df_parking_machine_learning.drop(
        "parking_id", "hour", "minutes", "day").orderBy("datetime")

    vectorAssembler = VectorAssembler(
        inputCols=["parking_temperature", "parking_humidity",
                   "area_total_spots", "parking_wind_speed",
                   "parking_closed", "parking_holiday_status",
                   "area_available_spots", "area_occupied_spots",
                   "slot_state"],
        outputCol='features')

    va_df_parking = vectorAssembler.transform(df_parking_machine_learning)
    va_df_parking = va_df_parking \
        .select(['datetime', "level_id",
                 "area_id", "slot_id",
                 'features', 'area_occupation_percentage'])

    train_df, test_df = va_df_parking.randomSplit([0.7, 0.3])

    lr = LinearRegression(featuresCol='features', labelCol='area_occupation_percentage',
                          maxIter=10, regParam=0.3, elasticNetParam=0.8)
    lr_model = lr.fit(train_df)
    print("Coefficients: " + str(lr_model.coefficients))
    print("Intercept: " + str(lr_model.intercept))

    trainingSummary = lr_model.summary
    print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
    print("r2: %f" % trainingSummary.r2)

    lr_predictions = lr_model.transform(test_df)

    lr_evaluator = RegressionEvaluator(predictionCol="prediction",
                                       labelCol="area_occupation_percentage", metricName="r2")
    print("R Squared (R2) on test data = %g" %
          lr_evaluator.evaluate(lr_predictions))

    predictions = lr_model.transform(test_df)
    predictions = predictions.select("datetime", "level_id", "area_id",
                                     "slot_id", "prediction", "area_occupation_percentage",
                                     "features") \
        .withColumnRenamed("prediction", "area_occupation_percentage_target")

    predictions = predictions \
        .dropDuplicates((['datetime', 'level_id', 'area_id'])) \
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

    receiver = "pedrobonillo15@gmail.com; diazjose_80@hotmail.com; juandmattos@gmail.com"
    mail_content = f'''Estimado Soporte,<br><br>
    El modelo de Machine Learning para el parking de <b>{parking}</b> a finalizado con <b>éxito</b>!!!<br>
    Saludos Cordiales,<br>
    Smart Parking System<br><br>
    <i><b>NOTA:</b> este mensaje es generado de forma automática por la plataforma de monitoreo, no es necesaria la respuesta de este mail!!.<i>'''
    enviar_mail(subject="[INFO] Modelo de Machine Learning finalizado con EXITO!!",
                receiver_address=receiver, mail_content=mail_content)


if __name__ == '__main__':
    main()
