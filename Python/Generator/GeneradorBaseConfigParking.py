import os 
import sys 
import uuid
import json
import getopt
from datetime import datetime
from venv import create
import argparse
from geopy.geocoders import Nominatim 

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--parking",
        help="Parking Name",
        dest="parking",
        choices=["PuntaCarretasShopping", "TresCrucesShopping"],
        required=True,
    )

    parser.add_argument(
        "-d",
        "--description",
        help="Parking description",
        dest="description",
        required=True,
    )

    parser.add_argument(
        "-a",
        "--address",
        help="Parking address",
        dest="address",
        required=True,
    )

    parser.add_argument(
        "-i",
        "--id",
        help="Parking ID",
        dest="id",
        required=True,
    )

    parser.add_argument(
        "-c",
        "--create",
        help="Create Action device",
        dest="create",
        default=bool,
        required=True,
    )

    return parser.parse_args()


def normalize_string(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("Á", "A"),
        ("É", "E"),
        ("Í", "I"),
        ("Ó", "O"),
        ("Ú", "U"),
    )
    for a, b in replacements:
        s = s.replace(a, b)
    return s

def main():
    print("""
    Bienvenido a la primer Script del Proyecto SmartParkingSystem
    este script esta diseñado para la generación de un nuevo Parking
    para la integración dentro del Sistema de BigData\n\n""")

    dirGeneral = "/opt/data/Generator/Parkings/"

    parking_uuid = uuid.uuid4().urn.split(":")[-1]

    args = get_args()
    parking_name = args.parking
    parking_description = args.description
    parking_address = args.address
    parking_id = args.id
    create_opt = args.create
    print(create_opt, parking_address, parking_description, parking_name, parking_id)

    if parking_name == "" or parking_address == "" or parking_description == "" or parking_id == "":
        print("Las opciones --description (-d), --address (-a), --name (-n) y --id (-i) son obligatorias...")
        sys.exit()
    else:
        contenido = os.listdir(dirGeneral)
        # # Rutina de creación de Parking 
        geolocator = Nominatim(user_agent="Parking_point")
        location = geolocator.geocode(parking_address) 

        if create_opt and "BaseConfig" in contenido:
            
            os.makedirs(dirGeneral+parking_name+"/ActiveDevices",  exist_ok=True)
            os.system("cp -r /opt/smart-parking/Python/Generator/BaseConfig/producerBaseConfig.json "+dirGeneral+parking_name+"/producer"+parking_name+".json")

            with open(dirGeneral+parking_name+"/producer"+parking_name+".json", "r") as file:
                data = json.load(file)

            data.update(parking_address=normalize_string(location.address),
                        parking_description=parking_description,
                        parking_name=parking_name,
                        parking_latitude=location.latitude,
                        parking_longitude=location.longitude,
                        parking_uuid=parking_uuid,
                        parking_id=parking_id)
            json_data = json.dumps(data)
            
            with open(dirGeneral+parking_name+"/producer"+parking_name+".json", "w") as file:
                file.write(json_data)
        else:
            #  print information for the creation
            print(parking_name)
            print(parking_description)
            print(location.address.encode("UTF-8"))
            print(create_opt)
            print(parking_id)
            print(location.latitude)
            print(location.longitude)
            print(parking_uuid)
            pass
            
            
    
    
if __name__ == '__main__':
    main()
