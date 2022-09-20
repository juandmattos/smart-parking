import requests
import json
import time
from datetime import datetime, timedelta
import getopt
import sys

dirGenral = '/opt/data/GetData/Parkings/'

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


def main():
    try:
        parking = getParameters(sys.argv[1:])
        while True:
            try:
                with open(dirGenral+parking+"/"+parking+"Data.json", 'r') as f:
                    row = json.load(f)
                # parking_timestamp = datetime.strptime(row['parking_timestamp'], "%d/%m/%Y|%H:%M:%S")
                # parking_timestamp_start_closed = datetime(parking_timestamp.year, parking_timestamp.month, parking_timestamp.day, 22, 00)
                # parking_timestamp_end_closed = datetime(parking_timestamp.year, parking_timestamp.month, parking_timestamp.day, 8, 00) + timedelta(days=1) 
                # if parking_timestamp
                response = requests.post('https://smart-parking-ort-db.herokuapp.com/api/v1/parkings/'+row["parking_id"], json=row)
                #print(response)
            except Exception as e:
                print(e)
            
            time.sleep(1)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()