
from xml.etree.ElementPath import find
import findspark
import os
import sys
import json
import getopt
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

dirGeneral = "/opt/data/GetData/Parkings/"

findspark.init(spark_home='/opt/spark')

def getParameters(argv):
    global dirGeneral
    try:
        opts, args = getopt.getopt(argv, "h:p", ["help", "parking="])
    except getopt.GetoptError:
        print("Opcion no valida")
        usage()            
        sys.exit(2)   
    
    parking = ""
    for opt, arg in opts:
        if opt in ("-h", "--help"):      
            usage()               
            sys.exit()                  
        elif opt in ('-p', "--parking"):
            parking = arg
            if " " in parking:
                print("The parking name should be without space... Try Again!!")
                usage()
                sys.exit()

    if parking == "" :
        print("Parking parameter is Mandatory... Try Again!!")
        usage()
        sys.exit()
    else:
        return parking

def usage():
    print("""
    Opciones:
    --help (-h)\t\tAvailable options
    --parking (-p)\t\tParking Name (Mandatory)
    """)

def percentageOcuppation(sp_total, sp_ocupied):
    percnt = int((sp_ocupied*100)/sp_total)
    return percnt

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

class ForeachWriter:
    def open(self, partition_id, epoch_id):
        return True

    def process(self, row):
        # Write row to connection. This method is NOT optional in Python.
        
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
        row['area_occupation_percentage'] = percentageOcuppation(int(totalSpots), occu)
        
        row['area_available_spots'] = str(int(totalSpots) - occu)
        row['area_occupied_spots'] = str(occu)
        row['area_total_spots'] = totalSpots
        areaInfo = {}
        areaInfo.update(area_id=row['device_area_id'],area_name=row['device_area_name'],area_description="shot description",
                        area_occupation=row['area_occupation'], area_occupied_spots=row['area_occupied_spots'],
                        area_total_spots=row['area_total_spots'], area_available_spots=row['area_available_spots'], 
                        area_occupation_percentage=str(row['area_occupation_percentage'])) 
        #device area_color
        if row['device_area_name'] == "A":
            areaInfo.update(area_color="#3244a8", area_description="blue")
        elif row['device_area_name'] == "B":
            areaInfo.update(area_color="#cf852b", area_description="orange")
        elif row['device_area_name'] == "C":
            areaInfo.update(area_color="#9319bf", area_description="purple")
        elif row['device_area_name'] == "D":
            areaInfo.update(area_color="#a67a5b", area_description="Light Brown")
        else:
            areaInfo.update(area_color="#ffffff", area_description="black")

        with open("/opt/data/GetData/Parkings/"+row["parking_name"]+'/area_summary.json', 'r') as f:
            dictAreaSummary = json.load(f)

        areaInfo.update(area_summary=dictAreaSummary)
        slotsInfo = []
        area_price = 0
        for slot in row['slotsUpdated']:
            SLTINFO = {}
            SLTINFO['slot_id'] = slot[0]
            SLTINFO['slot_state'] = slot[1]
            SLTINFO['slot_description'] = slot[0]+row['device_area_name'].upper()
            SLTINFO['slot_price'] = "200"
            if row['device_area_name'] == "A" and row['device_level_id'] == "1":
                SLTINFO['slot_type'] = "motorcycles"
            elif row['device_area_name'] == "B" and row['device_area_name'] == "C" and row['device_level_id'] == "1" and int(slot[0]) < 5:
                SLTINFO['slot_type'] = "trucks"
            else:
                SLTINFO['slot_type'] = "cars"
            #POSIBLE INTEGRACION
            # if slot[1]:
            #     SLTINFO['slot_price'] = "200"
            # else:
            #     SLTINFO['slot_price'] = ""
            area_price += int(SLTINFO['slot_price'])
            slotsInfo.append(SLTINFO)
        areaInfo['area_average_price'] = str(int(area_price/int(row['area_total_spots'])))
        #print(areaInfo)
        areaInfo.update(slots=slotsInfo)
    
        # AREAS DATA
        with open("/opt/data/GetData/Parkings/"+row["parking_name"]+'/Areas/areasLevel'+row['device_level_id']+'.json', 'r') as f:
            JsonAreas = json.load(f)  

        for i in range(len(JsonAreas['areas'])):
            if str(areaInfo['area_id']) == JsonAreas['areas'][i]['area_id'] and str(areaInfo['area_name']) == JsonAreas['areas'][i]['area_name']:
                JsonAreas['areas'][i] = areaInfo
                    
        with open("/opt/data/GetData/Parkings/"+row["parking_name"]+'/Areas/areasLevel'+row['device_level_id']+'.json', 'w') as f:
            f.write(json.dumps(JsonAreas))
        
        ## LEVELS DATA
        levelInfo = {}
        levelInfo.update(level_id=row['device_level_id'], level_name="Piso "+row['device_level_id']) 

        sumaOccuLevelSlots = 0
        sumaAvailableLevelSlots = 0
        sumaTotalLevelSlots = 0
        sumaTotalPriceLevel = 0
        for area in JsonAreas['areas']:
            if "area_occupied_spots" in area:
                sumaOccuLevelSlots += int(area['area_occupied_spots'])
                sumaTotalLevelSlots += int(area['area_total_spots'])
                sumaAvailableLevelSlots += int(area['area_available_spots'])
                sumaTotalPriceLevel += int(area['area_average_price'])
        
        # TO DO
        levelInfo['level_average_price'] = str(sumaTotalLevelSlots / len(JsonAreas['areas']))
        levelInfo.update(level_occupation=percentagetoString(sumaTotalLevelSlots, sumaOccuLevelSlots), level_occupied_spots=str(sumaOccuLevelSlots),
            level_available_spots= str(sumaAvailableLevelSlots),level_total_spots=str(sumaTotalLevelSlots),
            level_occupation_percentage=str(percentageOcuppation(sumaTotalLevelSlots, sumaOccuLevelSlots)), areas=JsonAreas['areas'])

        #levelInfo.update(level_occupation=percentagetoString(sumaTotalLevelSlots, sumaOccuLevelSlots), level_occupied_slots=sumaOccuLevelSlots,
        #                level_total_slots=sumaTotalLevelSlots, areas=JsonAreas['areas'])
        
        with open("/opt/data/GetData/Parkings/"+row["parking_name"]+'/'+row["parking_name"]+'Levels.json', 'r') as f:
            JsonLevels = json.load(f)  
        #print(JsonLevels)
        for i in range(len(JsonLevels['levels'])):
            if str(levelInfo['level_id']) == JsonLevels['levels'][i]['level_id']:
                JsonLevels['levels'][i] = levelInfo
                    
        with open("/opt/data/GetData/Parkings/"+row["parking_name"]+'/'+row["parking_name"]+'Levels.json', 'w') as f:
            f.write(json.dumps(JsonLevels))
        
        parkingInfo = {"parking_id": row["parking_id"]}
        
        if row['parking_name'] == "TresCrucesShopping":
            parkingInfo.update(parking_name="Shopping Tres Cruces")
        elif row['parking_name'] == "PuntaCarretasShopping":
            parkingInfo.update(parking_name="Shopping Punta Carretas")
        else:
            parkingInfo.update(parking_name=row['parking_name'])

        parkingInfo.update(parking_description=row['parking_description'],
            parking_address=row['parking_address'], parking_closed=False, parking_latitude=str(row['parking_latitude']),
            parking_longitude=str(row['parking_longitude']), parking_weather_status=row['parking_weather_status'],
            parking_weather_status_detailed=row['parking_weather_status_detailed'], parking_wind_speed=row['parking_wind_speed'],
            parking_holiday_status=row['parking_holiday_status'], parking_holiday_description=row['parking_holiday_description'],
            parking_holiday_type=row['parking_holiday_type'])
        parkingInfo['parking_timestamp'] = datetime.now().strftime("%d/%m/%Y|%H:%M:%S")
        

        with open("/opt/data/GetData/Parkings/"+row["parking_name"]+'/MachineLearning/ParkingSummary.json', 'r') as f:
            parking_summary = json.load(f)  
        
        parkingInfo['parking_summary'] = parking_summary
        
        parkingInfo.update(levels=JsonLevels['levels'])

        with open("/opt/data/GetData/Parkings/"+row["parking_name"]+'/'+row["parking_name"]+'Data.json', 'w') as f:
            f.write(json.dumps(parkingInfo))
        
        return True
        
    def close(self, error):
        # Close the connection. This method in optional in Python.
        #print(error)
        pass

def main():
    parking = getParameters(sys.argv[1:])
    findspark.init()
    spark_dir_utils = "/opt/smart-parking/Python/Spark-Jars-Utils/"
    spark = (SparkSession
            .builder
            .master('local[*]')
            .appName(parking+"ToBackend")
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

    contenido = os.listdir(dirGeneral+parking)
    if "config.json" not in contenido:
        print(" archivo config.json no se encuentra en directorio")
        sys.exit()

    try:
        print("\nEl parking seleccionado es - "+parking)  
        print("\n Cargando la configuracion necesaria para el consumo al backend")
        print("esta operacion puede tomar unos minutos...")
        
        with open(dirGeneral+parking+"/config.json", 'r') as f:
            baseConfigJson = json.load(f)
        
        #cargado de config para los levels...
        levels = [{"level_id": str(i+1)} for i in range(int(baseConfigJson['levels']))]
        with open(dirGeneral+parking+"/"+parking+"Levels.json", "w") as f:
            f.write(json.dumps({"levels": levels}))
            
        for i in range(len(baseConfigJson["areas"])):
            with open(dirGeneral+parking+"/Areas/areasLevel"+str(i+1)+".json", "w") as f:
                f.write(json.dumps({'areas':baseConfigJson["areas"][i]['areas_level_'+str(i+1)]}))
        
        df \
        .writeStream \
        .foreach(ForeachWriter()) \
        .start() \
        .awaitTermination()
    except Exception as e:
        print(e)
        sys.exit()

if __name__ == '__main__':
    main()
