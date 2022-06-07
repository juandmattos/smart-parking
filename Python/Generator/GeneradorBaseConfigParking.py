import os 
import sys 
import uuid
import json
import getopt
from datetime import datetime
from venv import create
from geopy.geocoders import Nominatim 

def getParameters(argv):
    try:
        opts, args = getopt.getopt(argv, "h:d:a:n:i:c", ["help", "description=", "address=", "name=", "id=", "create"])
    except getopt.GetoptError:
        print("Opcion no valida")
        usage()            
        sys.exit(2)   
    
    create = False
    description = ""
    address = ""
    name = ""
    id = ""
    for opt, arg in opts:
        if opt in ("-h", "--help"):      
            usage()               
            sys.exit()                  
        elif opt in ('-d', "--description"):
            description = arg
            print(description)
        elif opt in ('-a', "--address"):
            address = arg
        elif opt in ('-n', "--name"):
            name = arg.replace(" ", "")
        elif opt in ('-c', "--create"):
            create = True
        elif opt in ('-i', '--id'):
            id = arg
    return create, description, address, name, id

def usage():
    print("""
Opciones:
--help (-h)\t\tMenu de Opciones del programa
--description (-d)\t\tDescripcion del parking (Mandatorio)
--address (-a)\t\tNombre de la Calle y numero de puerta del Parking (Mandatorio)
--name (-n)\t\tNombre del Parking (Mandatorio)
--id (-i)\t\tID del parking(Mandatorio)
--create (-c)\t\tFuncion de creacion del directorio del parking
""")

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

    dirGeneral = "/opt/smart-parking/Python/Generator/"

    parking_uuid = uuid.uuid4().urn.split(":")[-1]
    create_opt, parking_description, parking_address, parking_name, parking_id = getParameters(sys.argv[1:])
    print(create_opt, parking_address, parking_description, parking_name, parking_id)

    if parking_name == "" or parking_address == "" or parking_description == "" or parking_id == "":
        print("Las opciones --description (-d), --address (-a), --name (-n) y --id (-i) son obligatorias...")
        usage()
        sys.exit()
    else:
        contenido = os.listdir(dirGeneral)
        # # Rutina de creación de Parking 
        geolocator = Nominatim(user_agent="Parking_point")
        location = geolocator.geocode(parking_address) 

        if create_opt and "BaseConfig" in contenido:
            
            os.makedirs(dirGeneral+"Parkings/"+parking_name+"/ActiveDevices",  exist_ok=True
            
            )
            os.system("cp -r "+dirGeneral+"BaseConfig/producerBaseConfig.json "+dirGeneral+"Parkings/"+parking_name+"/producer"+parking_name+".json")

            with open(dirGeneral+"Parkings/"+parking_name+"/producer"+parking_name+".json", "r") as file:
                data = json.load(file)

            data.update(parking_address=normalize_string(location.address),
                        parking_description=parking_description,
                        parking_name=parking_name,
                        parking_latitude=location.latitude,
                        parking_longitude=location.longitude,
                        parking_uuid=parking_uuid, 
                        parking_id=parking_id)
            json_data = json.dumps(data, indent = 2)
            
            with open(dirGeneral+"Parkings/"+parking_name+"/producer"+parking_name+".json", "w") as file:
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
