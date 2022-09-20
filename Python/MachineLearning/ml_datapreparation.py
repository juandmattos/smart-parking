#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import findspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions  as fn
from datetime import datetime
from kafka import KafkaConsumer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

global parking

def enviar_mail(receiver_address:str, subject :str, mail_content:str,
                sender_address = 'smartpsystem@gmail.com', 
                ):   
    
    sender_pass = 'vtyrkfqciworubfg'

    try:
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = subject  #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as excep:
        print('Exception: '+excep)
        print('Mail not sent!!. ')

def main():
    os.environ["HADOOP_USER_NAME"] = "hadoop"
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
             .appName('ml_'+parking+'_data_preparation')
             .getOrCreate())

    spark.sparkContext.setLogLevel("ERROR")
    sc = spark.sparkContext

    now = datetime.now()
    df_parking = spark.read.parquet(f"hdfs://hadoop-namenode:9000/data/Parkings/{parking}/year={now.year}/month={now.month - 1}/")
    
    df_parking_cleaned = df_parking \
            .withColumn("year", fn.year(fn.col("device_timestamp"))) \
            .withColumn("month", fn.month(fn.col("device_timestamp"))) \
            .withColumn("day", fn.dayofmonth(fn.col("device_timestamp"))) \
            .withColumn("parking_temperature", fn.col("parking_temperature").cast("double"))\
            .withColumn("parking_humidity", fn.col("parking_humidity").cast("double"))\
            .withColumn("slot_state", fn.col("slot_state").cast("integer")) \
            .withColumn("parking_closed", fn.col("parking_closed").cast("integer")) \
            .withColumn("parking_holiday_status", fn.col("parking_holiday_status").cast("integer")) \
            .drop("device_slots", 
                  "parking_address",
                  "parking_description",
                  "parking_weather_status_detailed",
                  "parking_uuid",
                  "parking_holiday_description",
                  "level_name",
                  "area_occupation",
                  "device_timestamp",
                  "parking_latitude",
                  "parking_longitude"
            )

    df_parking_cleaned.createOrReplaceTempView("tres_cruces_shopping")

    parking_cleaned = spark.sql("""
        SELECT
            DISTINCT(
                tcs.year,
                tcs.month,
                tcs.day,
                tcs.hour, 
                tcs.minutes, 
                tcs.device_id, 
                tcs.level_id, 
                tcs.area_id, 
                tcs.slot_id
            ) as MASTER_KEY,
            CAST(
                CONCAT(
                    "2022-7-",
                    tcs.day, 
                    " ", 
                    tcs.hour, 
                    ":", 
                    tcs.minutes, 
                    ":00"
                ) as timestamp
            ) as datetime,
            tcs.*
        FROM
            tres_cruces_shopping tcs
        """).drop("MASTER_KEY", "parking_name")

    parking_cleaned \
        .write \
        .format("parquet") \
        .mode("overwrite") \
        .partitionBy("year", "month", "day") \
        .save("hdfs://hadoop-namenode:9000/machineLearning/Parkings/"+parking+"/")

    receiver = "pedrobonillo15@gmail.com; diazjose_80@hotmail.com; juandmattos@gmail.com"
    mail_content = f'''Estimado Smart Parking Administrator,<br><br>
    La preparacion de datos para el modelo de Machine Learning para el parking de <b>{parking}</b> a finalizado con <b>éxito</b>!!!<br>
    Saludos Cordiales,<br>
    Smart Parking System<br><br>
    <i><b>NOTA:</b> este mensaje es generado de forma automática por la plataforma de monitoreo, no es necesaria la respuesta de este mail!!.<i>'''
    enviar_mail(subject="[INFO] Preparacion de datos para Machine Learning finalizado con EXITO!!",
                receiver_address=receiver, mail_content=mail_content)
if __name__ == '__main__':
    main()
