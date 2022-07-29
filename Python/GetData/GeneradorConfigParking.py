import os
import shutil
import subprocess
import json 
import sys
from kafka import KafkaConsumer

dirGeneral = "/opt/data/GetData/Parkings/"

consumer = KafkaConsumer(bootstrap_servers=['hadoop-namenode'])
topics = list(consumer.topics())

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

### Generacion de config.json 
try:
    contenido = os.listdir(dirGeneral+parking)
    if "config.son" in contenido:
        print("Intente nuevamente... el archivo ya existia!!")
        sys.exit()
    else:
        niveles = input("Indique la cantidad de niveles que tiene el parking (2): ")
        niveles = 2 if niveles == "" else int(niveles)
        dict_json = {}
        dict_json['levels'] = niveles
        dict_json['areas'] = []
        for i in range(1, niveles+1):
            areaLevel = {}
            areaLevel['areas_level_'+str(i)] = []
            area_por_level = input("Indique las areas para el nivel "+str(i)+" (1-A, 1-B, ...): ")
            area_por_level = area_por_level.replace(" ", "")
            # "1-A,1-B,1-C"
            for area in area_por_level.split(","):
                area_aux = {}
                area_id = area.split("-")[0]
                area_name = area.split("-")[1]
                area_aux['area_id'] = area_id
                area_aux['area_name'] = area_name
                areaLevel['areas_level_'+str(i)].append(area_aux)
            dict_json['areas'].append(areaLevel)
        print(json.dumps(dict_json, indent=2))
        with open(dirGeneral+parking+'/config.json', 'w') as f:
            f.write(json.dumps(dict_json, indent = 2))
except Exception as e:
    print(e)
    shutil.rmtree(dirGeneral+parking)