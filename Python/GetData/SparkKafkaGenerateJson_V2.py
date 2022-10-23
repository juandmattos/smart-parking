
import time
from xml.etree.ElementPath import find
import findspark
import os
import sys
import json
import argparse
import psycopg2
from datetime import datetime
#from sqlalchemy import create_engine
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

dirGeneral = "/opt/data/GetData/Parkings"

#findspark.init(spark_home='/opt/spark')

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
        
        #engine = create_engine('postgresql+psycopg2://pi:apice868@hostname/database_name')
        self.conn = psycopg2.connect(database="postgres",
                        host="192.168.68.109",
                        user="pi",
                        password="apice868",
                        port="5432")
        self.cursor = self.conn.cursor()

        return True

    def process(self, row):
        # Write row to connection. This method is NOT optional in Python.
        try:
            
            row = json.loads(row['value'].decode("UTF-8"))

            self.cursor.execute(f"SELECT data FROM public.parkingsdata WHERE parking_name = '{row['parking_name']}'")
            data = dict(self.cursor.fetchone()[0])

            data.update(parking_id=row["parking_id"], parking_description=row['parking_description'],
            parking_address=row['parking_address'], parking_closed=False, parking_latitude=str(row['parking_latitude']),
            parking_longitude=str(row['parking_longitude']), parking_weather_status=row['parking_weather_status'],
            parking_weather_status_detailed=row['parking_weather_status_detailed'], parking_wind_speed=row['parking_wind_speed'],
            parking_holiday_status=row['parking_holiday_status'], parking_holiday_description=row['parking_holiday_description'],
            parking_holiday_type=row['parking_holiday_type'], parking_timestamp=datetime.now().strftime("%d/%m/%Y|%H:%M:%S"))

            with open("/opt/data/GetData/Parkings/"+row["parking_name"]+'/MachineLearning/ParkingSummary.json', 'r') as f:
                parking_summary = json.load(f)  

            data['parking_summary'] = parking_summary
            
            level_id = int(row['device_level_id'])
            area_id = int(row['device_area_id'])
            area_name = row['device_area_name']
            #print(row)
            totalSpots = row["device_spots"]
            row['slotsUpdated'] = []
            occu = 0
            for i in range(int(totalSpots)):
                if row["device_slots"][i] == True:
                    occu += 1
                row['slotsUpdated'].append((str(i+1), row["device_slots"][i]))
            
            slotsInfo = []
            area_price = 0
            for slot in row['slotsUpdated']:
                SLTINFO = {}
                SLTINFO['slot_id'] = slot[0]
                SLTINFO['slot_state'] = slot[1]
                SLTINFO['slot_description'] = slot[0]+area_name.upper()
                SLTINFO['slot_price'] = "200"
                if area_name.upper() == "A" and level_id == 1:
                    SLTINFO['slot_type'] = "motorcycles"
                elif area_name.upper() == "B" or area_name.upper() == "C" and level_id == 1 and int(slot[0]) < 5:
                    SLTINFO['slot_type'] = "trucks"
                else:
                    SLTINFO['slot_type'] = "cars"
                area_price += int(SLTINFO['slot_price'])
                slotsInfo.append(SLTINFO)

            #print(slotsInfo)
            data['levels'][level_id - 1]['areas'][area_id -1].update(
                slots=slotsInfo, 
                area_occupation=percentagetoString(int(totalSpots), occu),
                area_occupation_percentage=percentageOcuppation(int(totalSpots), occu),
                area_available_spots=str(int(totalSpots) - occu), 
                area_occupied_spots=str(occu),
                area_total_spots=totalSpots,
                area_average_price=str(int(area_price/int(totalSpots)))
            )

            sumaOccuLevelSlots = 0
            sumaAvailableLevelSlots = 0
            sumaTotalLevelSlots = 0
            sumaTotalPriceLevel = 0
            for area in data['levels'][level_id - 1]['areas']:
                if "area_occupied_spots" in area:
                    sumaOccuLevelSlots += int(area['area_occupied_spots'])
                    sumaTotalLevelSlots += int(area['area_total_spots'])
                    sumaAvailableLevelSlots += int(area['area_available_spots'])
                    sumaTotalPriceLevel += int(area['area_average_price'])
            
            data['levels'][level_id - 1].update(
                level_occupation=percentagetoString(sumaTotalLevelSlots, sumaOccuLevelSlots), 
                level_occupied_spots=str(sumaOccuLevelSlots),
                level_available_spots= str(sumaAvailableLevelSlots),
                level_total_spots=str(sumaTotalLevelSlots),
                level_occupation_percentage=str(percentageOcuppation(sumaTotalLevelSlots, sumaOccuLevelSlots)),
                level_average_price = str(sumaTotalLevelSlots / len(data['levels'][level_id - 1]['areas']))
            )

            self.cursor.execute(f"UPDATE public.parkingsdata SET data = '{json.dumps(data)}' WHERE parking_name = '{row['parking_name']}'")
            #self.conn.close()
            return True
        except Exception as e:
            print("try again... ")
            print(e)
    
    
    def close(self, error):
        # Close the connection. This method in optional in Python.
        self.conn.close()
        print(error)
        pass


def processRow(row):
    # Write row to connection. This method is NOT optional in Python.

    conn = psycopg2.connect(database="postgres",
                        host="192.168.68.109",
                        user="pi",
                        password="apice868",
                        port="5432")
    cursor = conn.cursor()
    try:
        
        row = json.loads(row['value'].decode("UTF-8"))

        cursor.execute(f"SELECT data FROM public.parkingsdata WHERE parking_name = '{row['parking_name']}'")
        data = dict(cursor.fetchone()[0])

        data.update(parking_id=row["parking_id"], parking_description=row['parking_description'],
        parking_address=row['parking_address'], parking_closed=False, parking_latitude=str(row['parking_latitude']),
        parking_longitude=str(row['parking_longitude']), parking_weather_status=row['parking_weather_status'],
        parking_weather_status_detailed=row['parking_weather_status_detailed'], parking_wind_speed=row['parking_wind_speed'],
        parking_holiday_status=row['parking_holiday_status'], parking_holiday_description=row['parking_holiday_description'],
        parking_holiday_type=row['parking_holiday_type'], parking_timestamp=datetime.now().strftime("%d/%m/%Y|%H:%M:%S"), 
        parking_timestamp_2=datetime.now().strftime("%Y-%m-%d %T"))

        with open("/opt/data/GetData/Parkings/"+row["parking_name"]+'/MachineLearning/ParkingSummary.json', 'r') as f:
            parking_summary = json.load(f)  

        data['parking_summary'] = parking_summary
        
        level_id = int(row['device_level_id'])
        area_id = int(row['device_area_id'])
        area_name = row['device_area_name']
        #print(row)
        totalSpots = row["device_spots"]
        row['slotsUpdated'] = []
        occu = 0
        for i in range(int(totalSpots)):
            if row["device_slots"][i] == True:
                occu += 1
            row['slotsUpdated'].append((str(i+1), row["device_slots"][i]))
        
        slotsInfo = []
        area_price = 0
        for slot in row['slotsUpdated']:
            SLTINFO = {}
            SLTINFO['slot_id'] = slot[0]
            SLTINFO['slot_state'] = slot[1]
            SLTINFO['slot_description'] = slot[0]+area_name.upper()
            SLTINFO['slot_price'] = "200"
            if area_name.upper() == "A" and level_id == 1:
                SLTINFO['slot_type'] = "motorcycles"
            elif area_name.upper() == "B" or area_name.upper() == "C" and level_id == 1 and int(slot[0]) < 5:
                SLTINFO['slot_type'] = "trucks"
            else:
                SLTINFO['slot_type'] = "cars"
            area_price += int(SLTINFO['slot_price'])
            slotsInfo.append(SLTINFO)

        #print(slotsInfo)
        data['levels'][level_id - 1]['areas'][area_id -1].update(
            slots=slotsInfo, 
            area_occupation=percentagetoString(int(totalSpots), occu),
            area_occupation_percentage=percentageOcuppation(int(totalSpots), occu),
            area_available_spots=str(int(totalSpots) - occu), 
            area_occupied_spots=str(occu),
            area_total_spots=totalSpots,
            area_average_price=str(int(area_price/int(totalSpots)))
        )

        sumaOccuLevelSlots = 0
        sumaAvailableLevelSlots = 0
        sumaTotalLevelSlots = 0
        sumaTotalPriceLevel = 0
        for area in data['levels'][level_id - 1]['areas']:
            if "area_occupied_spots" in area:
                sumaOccuLevelSlots += int(area['area_occupied_spots'])
                sumaTotalLevelSlots += int(area['area_total_spots'])
                sumaAvailableLevelSlots += int(area['area_available_spots'])
                sumaTotalPriceLevel += int(area['area_average_price'])
        
        data['levels'][level_id - 1].update(
            level_occupation=percentagetoString(sumaTotalLevelSlots, sumaOccuLevelSlots), 
            level_occupied_spots=str(sumaOccuLevelSlots),
            level_available_spots= str(sumaAvailableLevelSlots),
            level_total_spots=str(sumaTotalLevelSlots),
            level_occupation_percentage=str(percentageOcuppation(sumaTotalLevelSlots, sumaOccuLevelSlots)),
            level_average_price = str(sumaTotalLevelSlots / len(data['levels'][level_id - 1]['areas']))
        )

        #cursor.execute(f"UPDATE public.parkingsdata SET data = '{json.dumps(data)}', audit_time = NOW() WHERE parking_name = '{row['parking_name']}'")
        sql_update = "UPDATE public.parkingsdata SET data = %s, audit_time = NOW(), row_timestamp = %s WHERE parking_name = %s"
        cursor.execute(sql_update, (json.dumps(data), row['device_timestamp'], row['parking_name']))
        #updated_rows = cursor.rowcount
        #print(updated_rows)
        # Commit the changes to the database
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("try again... ")
        print(e)


def main():
    
    parser = argparse.ArgumentParser(description='Conexion a Kafka para transmitir a Backend')
    parser.add_argument('-p', '--parking', type=str, choices= ['TresCrucesShopping', 'PuntaCarretasShopping'], help='Parkings to consume')

    args = parser.parse_args()
    parking = args.parking
    findspark.init()
    
    spark = (SparkSession
            .builder
            .master('local[*]')
            .appName(parking+"ToBackend")
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

    try:
        df \
        .writeStream \
        .foreach(processRow) \
        .start() \
        .awaitTermination()
    except Exception as e:
        print(e)
        sys.exit()

if __name__ == '__main__':
    main()
