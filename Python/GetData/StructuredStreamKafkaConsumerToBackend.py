#!/usr/bin/env python
# coding: utf-8

# In[20]:


import subprocess
import findspark
import sys
import json 
import pandas as pd
import time 
import random
import os
import shutil
import requests
from datetime import datetime
from kafka import KafkaProducer
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window


# In[2]:


global dirGeneral
dirGeneral = "/opt/smart-parking/Python/GetData/Parkings/"

findspark.init(spark_home='/opt/spark')

topics = subprocess.check_output("/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server hadoop-namenode:9092", shell=True)
topics = topics.split()
topics = [ topic.decode("UTF-8") for topic in topics ]
topics.pop()
topics

op = 0
while True:
    print("Para realizar el consumo del Parking seleccione\nalguno de los siguientes topicos de Kafka...")
    for i in range(1,len(topics)+1):
        print(str(i)+".- "+topics[i-1])
    try:
        o = int(input("Indique su opcion: "))
        if topics[o-1]:
            parking = topics[o-1]
        break
    except IndexError:
        print("seleccione una opcion correcta... ")

try:
    shutil.rmtree(dirGeneral+parking)
except FileNotFoundError as error:
    print("Directorio no existe, se creará directorio asociado al parking...")

os.makedirs(dirGeneral+parking+"/Areas/", exist_ok=False)

while True:
    op = input("Indique si realizo la carga del archivo config.json en el directorio correspondiente al parking (S o N): ")
    if op.lower() == "s":
        contenido = os.listdir(dirGeneral+parking)
        if "config.json" in contenido:
            break
        else:
            print("no se ha encontrado archivo config.json...")
    else:
        print("seleccione una opcion valida...")

if parking:
    print("\nEl parking seleccionado es - "+parking)  
    print("\n Cargando la configuracion necesaria para el consumo al backend")
    print("esta operacion puede tomar unos minutos...")
    
    with open(dirGeneral+parking+"/config.json", 'r') as f:
        baseConfigJson = json.load(f)
    
    #cargado de config para los levels...
    levels = [{"level_id": str(i+1)} for i in range(int(baseConfigJson['levels']))]
    with open(dirGeneral+parking+"/"+parking+"Levels.json", "w") as f:
        f.write(json.dumps({"levels": levels}, indent = 2))
        
    for i in range(len(baseConfigJson["areas"])):
        with open(dirGeneral+parking+"/Areas/areasLevel"+str(i+1)+".json", "w") as f:
            f.write(json.dumps({'areas':baseConfigJson["areas"][i]['areas_level_'+str(i+1)]}, indent = 4))
            
            
    # Spark session & context
    spark = (SparkSession
             .builder
             .master('local[*]')
             .appName(parking+"Spark")
             .config('spark.jars', 'file:///opt/smart-parking/Python/Spark-Jars-Utils/spark-sql-kafka-0-10_2.12-3.2.1.jar,file:///opt/smart-parking/Python/Spark-Jars-Utils/kafka-clients-3.1.0.jar')
             .config('spark.executor.extraClassPath','file:///opt/smart-parking/Python/Spark-Jars-Utils/spark-sql-kafka-0-10_2.12-3.2.1.jar:file:///opt/smart-parking/Python/Spark-Jars-Utils/kafka-clients-3.1.0.jar')
             .config('spark.executor.extraLibrary','file:///opt/smart-parking/Python/Spark-Jars-Utils/spark-sql-kafka-0-10_2.12-3.2.1.jar:file:///opt/smart-parking/Python/Spark-Jars-Utils/kafka-clients-3.1.0.jar')
             .config('spark.driver.extraClassPath', 'file:///opt/smart-parking/Python/Spark-Jars-Utils/spark-sql-kafka-0-10_2.12-3.2.1.jar:file:///opt/smart-parking/Python/Spark-Jars-Utils/kafka-clients-3.1.0.jar')
             .getOrCreate())

    sc = spark.sparkContext
    sc.setLogLevel("ERROR")


    # Subscribe to 1 topic
    df = spark \
      .readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", "hadoop-namenode:9092") \
      .option("subscribe", parking) \
      .load()
    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
else:
    sys.exit()


# In[36]:


def percentagetoString(sp_total, sp_ocupied):
    percnt = int((sp_ocupied*100)/sp_total)
    #print(percnt)
    if percnt >= 0 and percnt <=25:
        return "Empty"
    elif percnt > 25 and percnt <=50:
        return "Almost Empty"
    elif percnt > 50 and percnt <=75:
        return "Almost Full"
    elif percnt > 75 and percnt <=100:
        return "Full"
    else:
        return "Other"

def process_row(row):
    producer = KafkaProducer(bootstrap_servers=['hadoop-namenode:9092'], api_version=(0,10,0))
    
    row = json.loads(row['value'].decode("UTF-8"))
    
    #Routine for Slots
    totalSpots = row["device_spots"]
    row['slotsUpdated'] = []
    occu = 0
    for i in range(len(row["device_slots"])):
        if row["device_slots"][i] == True:
            occu += 1
        row['slotsUpdated'].append((str(i+1), row["device_slots"][i]))
    row['area_occupation'] = percentagetoString(int(totalSpots), occu)
    
    row['area_available_spots'] = str(int(totalSpots) - occu)
    row['area_occupied_spots'] = str(occu)
    row['area_total_spots'] = totalSpots
    areaInfo = {}
    areaInfo.update(area_id=row['device_area_id'],area_name=row['device_area_name'],area_description="shot description",
                    area_occupation=row['area_occupation'], area_occupied_spots=row['area_occupied_spots'],
                    area_total_spots=row['area_total_spots'], area_available_spots=row['area_available_spots']) 
    
    #TO DO
    areaInfo['area_average_price'] = "200"
    
    slotsInfo = []
    for slot in row['slotsUpdated']:
        SLTINFO = {}
        SLTINFO['slot_id'] = slot[0]
        SLTINFO['slot_state'] = slot[1]
        #TO DO
        SLTINFO['slot_price'] = "200"
        slotsInfo.append(SLTINFO)
    
    areaInfo.update(slots=slotsInfo)
   
    # AREAS DATA
    with open("/opt/smart-parking/Python/GetData/Parkings/"+row["parking_name"]+'/Areas/areasLevel'+row['device_level_id']+'.json', 'r') as f:
        JsonAreas = json.load(f)  

    for i in range(len(JsonAreas['areas'])):
        if str(areaInfo['area_id']) == JsonAreas['areas'][i]['area_id'] and str(areaInfo['area_name']) == JsonAreas['areas'][i]['area_name']:
            JsonAreas['areas'][i] = areaInfo
                
    with open("/opt/smart-parking/Python/GetData/Parkings/"+row["parking_name"]+'/Areas/areasLevel'+row['device_level_id']+'.json', 'w') as f:
        f.write(json.dumps(JsonAreas, indent = 2))
    
    ## LEVELS DATA
    levelInfo = {}
    levelInfo.update(level_id=row['device_level_id'], level_name="Piso "+row['device_level_id']) 
    
    # TO DO
    levelInfo['level_average_price'] = "200"

    sumaOccuLevelSlots = 0
    sumaAvailableLevelSlots = 0
    sumaTotalLevelSlots = 0
    for area in JsonAreas['areas']:
        if "area_occupied_spots" in area:
            sumaOccuLevelSlots += int(area['area_occupied_spots'])
            sumaTotalLevelSlots += int(area['area_total_spots'])
            sumaAvailableLevelSlots += int(area['area_available_spots'])
        
    
    levelInfo.update(level_occupation=percentagetoString(sumaTotalLevelSlots, sumaOccuLevelSlots), level_occupied_spots=sumaOccuLevelSlots,
                    level_available_spots= str(sumaAvailableLevelSlots),level_total_spots=str(sumaTotalLevelSlots), areas=JsonAreas['areas'])
    
    #levelInfo.update(level_occupation=percentagetoString(sumaTotalLevelSlots, sumaOccuLevelSlots), level_occupied_slots=sumaOccuLevelSlots,
    #                level_total_slots=sumaTotalLevelSlots, areas=JsonAreas['areas'])
    
    with open("/opt/smart-parking/Python/GetData/Parkings/"+row["parking_name"]+'/'+row["parking_name"]+'Levels.json', 'r') as f:
        JsonLevels = json.load(f)  
    #print(JsonLevels)
    for i in range(len(JsonLevels['levels'])):
        if str(levelInfo['level_id']) == JsonLevels['levels'][i]['level_id']:
            JsonLevels['levels'][i] = levelInfo
                
    with open("/opt/smart-parking/Python/GetData/Parkings/"+row["parking_name"]+'/'+row["parking_name"]+'Levels.json', 'w') as f:
        f.write(json.dumps(JsonLevels, indent = 2))
    
    parkingInfo = {"parking_id": row["parking_id"]}
    parkingInfo.update(parking_name=row['parking_name'], parking_description=row['parking_description'],
                      parking_address=row['parking_address'], parking_closed=False, parking_latitude=str(row['parking_latitude']),
                      parking_longitude=str(row['parking_longitude']), levels=JsonLevels['levels'])
    parkingInfo['parking_timestamp'] = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    
    # print(datetime.strptime(datetime.now(), "%Y-%m-%d %H:%M"))
    #producer.send("Parkings", value=json.dumps(parkingInfo).encode('utf-8'))
    #producer.close()
    
    r = requests.post('https://smart-parking-ort-db.herokuapp.com/api/v1/parkings/'+row["parking_id"], json=parkingInfo)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")
    
    print(parkingInfo['parking_timestamp'])
    #print(json.dumps(parkingInfo, indent = 2))
    
    #time.sleep(1)
    


# In[ ]:


df \
.writeStream\
.outputMode("append") \
.foreach(process_row) \
.start()\
.awaitTermination()


# In[ ]:




