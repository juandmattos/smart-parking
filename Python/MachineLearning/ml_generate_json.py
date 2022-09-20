#!/usr/bin/env python
# coding: utf-8

import os
import json
import argparse
import findspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as fn
from datetime import datetime
from kafka import KafkaConsumer

global parking

def generate_json(df: list, parking:str, basefile: str = "/opt/smart-parking/Python/MachineLearning/ParkingSummary.json"):
    try:
        with open(basefile) as file:
            json_file = json.load(file)
        
        data_dict = {}
        for row in df:
            if row['level_id'] in data_dict:
                data_dict[row['level_id']].append({'area_id': row['area_id'], 
                                        'area_occupation_percentage_target': round(row['area_occupation_percentage_target'])})
            else:
                data_dict.update({row['level_id']:[]})
                data_dict[row['level_id']].append({'area_id': row['area_id'], 
                                        'area_occupation_percentage_target': round(row['area_occupation_percentage_target'])})
            
        levels_object = []
        for k, v in data_dict.items():
            levels_object.append({'level_id': k, 'areas': v})
        
        json_file['levels'] = levels_object

        with open(f"/opt/data/GetData/Parkings/{parking}/MachineLearning/ParkingSummary.json", 'w') as f:
            f.write(json.dumps(json_file)) 
        
        return True
    except Exception as e:
        print(e)
        return False

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
    now = datetime.now()
    
    if now.hour > 8 and now.hour < 23:
        # Spark session & context
        spark = (SparkSession
                .builder
                .master('local[*]')
                .appName('ml_'+parking+'_generate_json')
                .getOrCreate())

        spark.sparkContext.setLogLevel("ERROR")
        sc = spark.sparkContext

        
        df_parking_machine_learning = spark \
            .read \
            .parquet(f"hdfs://hadoop-namenode:9000/predictions/Parkings/{parking}/year={now.year}/month={now.month - 1}/day={now.day}/hour={now.hour}/minute={now.minute}")
            
        generate_json(df=df_parking_machine_learning, parking=parking)
    else:
        print(f"{parking} is closed")

if __name__ == '__main__':
    main()
