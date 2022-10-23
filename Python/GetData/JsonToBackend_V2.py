import requests
import json
import psycopg2
import argparse
import time
from datetime import datetime, timedelta
import getopt
import sys

dirGenral = '/opt/data/GetData/Parkings/'

def main():
    try:
        parser = argparse.ArgumentParser(description='Conexion a Kafka para transmitir a Backend')
        parser.add_argument('-p', '--parking', type=str, choices= ['TresCrucesShopping', 'PuntaCarretasShopping'], help='Parkings to consume')

        args = parser.parse_args()
        parking = args.parking

        conn = psycopg2.connect(database="postgres",
                        host="192.168.68.109",
                        user="pi",
                        password="apice868",
                        port="5432")
        cursor = conn.cursor()
        

        while True:
            try:

                cursor.execute(f"SELECT data FROM public.parkingsdata WHERE parking_name = '{parking}'")
                data = dict(cursor.fetchone()[0])

                # parking_timestamp = datetime.strptime(row['parking_timestamp'], "%d/%m/%Y|%H:%M:%S")
                # parking_timestamp_start_closed = datetime(parking_timestamp.year, parking_timestamp.month, parking_timestamp.day, 22, 00)
                # parking_timestamp_end_closed = datetime(parking_timestamp.year, parking_timestamp.month, parking_timestamp.day, 8, 00) + timedelta(days=1) 
                # if parking_timestamp
                response = requests.post('https://smart-parking-ort-db.herokuapp.com/api/v1/parkings/'+data["parking_id"], json=data)
                print(response)
            except Exception as e:
                print(e)
            
            time.sleep(1)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()