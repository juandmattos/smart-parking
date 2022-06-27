#!/usr/bin/env python
# coding: utf-8
import random
import json
import time
import os
import sys
import getopt
import pyowm
from kafka import KafkaProducer
from datetime import datetime, timedelta

# DIFERENTES RUTINAS DE ENTRADA Y DATOS NECESARIOS PARA SU USO
dirgeneral = "/opt/smart-parking/Python/Generator/Parkings/"

def getAvailableParkings(directorios):
    print("\nThe next are available parkings: \n")
    str_aux = ""
    for i in range(1, len(directorios)+1):
        str_aux = str(i)+".- "+directorios[i-1]+"\n"
    print(str_aux)

def getAvailabledevices(devices):
    print("\nThe next are available devices: \n")
    for i in range(1, len(devices)+1):
        line = devices[i-1]+"\n"
        print(str(i)+".- "+line)

def getParameters(argv):
    global dirgeneral
    try:
        opts, args = getopt.getopt(argv, "h:p:l:i:a:d:q", ["help", "parking=", "level-id=", "area-id=", "area-name=", "device", "qt-slots"])
    except getopt.GetoptError:
        print("Opcion no valida")
        usage()            
        sys.exit(2)   
    
    parking = ""
    device = ""
    qt_slots = ""
    level_id = ""
    area_id = ""
    area_name = ""
    for opt, arg in opts:
        if opt in ("-h", "--help"):      
            usage()               
            sys.exit()                  
        elif opt in ('-p', "--parking"):
            directorios = os.listdir(dirgeneral)
            parking = arg
            if " " in parking:
                print("The parking name should be without space... Try Again!!")
                getAvailableParkings(directorios)
                usage()
                sys.exit()
            if parking == "":
                print("The parking parameter is Mandatory... Try Again!!")
                getAvailableParkings(directorios)
                usage()
                sys.exit()
            if parking not in directorios:
                print("The Parking is not created as Directory... Try Again")
                getAvailableParkings()
                usage()
                sys.exit()
        elif opt in ('-d', "--device"):
            with open(dirgeneral+parking+'/'+parking+'Devices.txt', 'r') as f:
                devices = f.readlines()
            device = random.choice(devices) if device == "" else int(arg)
            device = device.replace("\n", "")
            devices = [k.replace("\n","") for k in devices]
            if device not in devices:
                print("The device is not in the Parking Devices List... Please, Try Again!!")
                getAvailabledevices(devices)
                sys.exit()
            
            if len(device) != 16:
                print("The device should have 16 length... Please, Try Again!!")
                getAvailabledevices(devices)
                sys.exit()

            devices.remove(device)
            with open(dirgeneral+parking+'/ActiveDevices/'+device+'.txt', 'w') as f:
                f.write("1\n")

            try:
                with open(dirgeneral+parking+'/AllActiveDevices.txt', 'a+') as f:
                    f.write(device+"\n")
            except:
                with open(dirgeneral+parking+'/AllActiveDevices.txt', 'w+') as f:
                    f.write(device)
            devices = [k+"\n" for k in devices]
            with open(dirgeneral+parking+'/'+parking+'Devices.txt', 'w') as f:
                f.writelines(devices)
        elif opt in ('-q', "--qt-slots"):
            qt_slots = 10 if qt_slots == "" else int(arg)
        elif opt in ('-l', "--level-id"):
            level_id = arg
            if level_id == "":
                print("Level ID is a Mandatory parameter... Try Again!!")
                usage()
                sys.exit()
        elif opt in ('-i', '--area-id'):
            area_id = arg
            if area_id == "":
                print("Area ID is a Mandatory parameter... Try Again!!")
                usage()
                sys.exit()
        elif opt in ('-a', '--area-name'):
            area_name = arg
            if area_name == "":
                print("Area Name is a Mandatory parameter... Try Again!!")
                usage()
                sys.exit()

    if parking == "" or level_id == "" or area_id == "" or area_name == "":
        print("Parking, Level-ID, Area-ID, Area-Name parameters are almost Mandatory... Try Again!!")
        usage()
        sys.exit()
    if qt_slots == "" or device == "":
        print("qt-slots and device parameters are necessary to run the Producer\n... Try Again with the next command:\n")
        print("'python3.10 Producer-Parkings-Kafka-Streaming_V3.py --qt-slots --device'")
        usage()
        sys.exit()
    
    return parking, device, qt_slots, level_id, area_id, area_name

def usage():
    print("""
    Opciones:
    --help (-h)\t\tAvailable options
    --parking (-p)\t\tParking Name (Mandatory)
    --device (-d)\t\tDevice that has the control of the slots behaviour 
    --qt-slots (-q)\t\tQuantity of slots 
    --level-id (-l)\t\tLevel ID (Mandatory)
    --area-id (-i)\t\tArea ID of the Level (Mandatory)
    --area-name (-a)\t\tArea Name of the Level (Mandatory)
    """)

def main():
    print("""

    Bienvenido al Tercer Script del Proyecto SmartParkingSystem,
    este script esta diseñado para la ejecución de un dispositivo virtual
    dentro de la red de estacionamientos en el sistema de BigData\n\n""")

    parking, device, num_puestos, nivel, area, areaName = getParameters(sys.argv[1:])
    #device = list_device[0]
    num_puestos = int(num_puestos)
    # FORMAT A JSON MODEL FOR PARKING
    with open(dirgeneral+parking+'/producer'+parking+'.json') as f:
        data = json.load(f)

    data['device_id'] = device
    data['device_spots'] = str(num_puestos)
    data['device_level_id'] = nivel 
    data['device_area_id'] = area 
    data['device_area_name'] = areaName

    # Values used to random function
    lista_estado_puestos = [False for n in range(1,num_puestos + 1)]
    lista_auxTemp = [0 for n in range(1, num_puestos + 1)]
    rango = [2, 5, 10, 20, 30, 45, 60, 120, 240]
    #rango = [1, 2]
    slot_states = [True, False]

    # Rangos de fechas para horario nocturno, en el cual los carros se encuentran dentro del Parking
    Turno_inicio = str(datetime.now().day) +'/'+str(datetime.now().month) +'/'+str(datetime.now().year) +' 22:00:00'
    Turno_final = str(datetime.now().day + 1) +'/'+str(datetime.now().month) +'/'+str(datetime.now().year) +' 08:00:00'

    # Obtener fecha de primera consulta para el tiempo
    APIKEY='055bcf46839359ea922b925c3d7cd860'        # your API Key here as string
    owm = pyowm.OWM(APIKEY)                       # Use API key to get data
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place('Montevideo,UY').weather
    getTimeWeather = datetime.now() + timedelta(minutes=30)
    data['parking_temperature'] = weather.temperature(unit='celsius')['temp']
    data['parking_humidity'] = weather.humidity
    data['device_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Initialize a Kafka Producer
    producer = KafkaProducer(bootstrap_servers=['hadoop-namenode:9092'], api_version=(0,10,0), value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    topic = data['parking_name']
    print("El Topico a consumir es - "+topic)


    # LOOP PARA ENVIAR DATOS A KAFKA
    while True:
        try:
            now = datetime.now()
            #print("NOW - " + str(now))
            
            with open(dirgeneral+parking+'/ActiveDevices/'+device+'.txt', 'r') as f:
                status = f.readline()
            if status == '0\n':
                break
            #print("Turno Inicial - "+Turno_inicio)
            #print("Turno Final - "+Turno_final)
            if now >= datetime.strptime(Turno_inicio, '%d/%m/%Y %H:%M:%S') and now <= datetime.strptime(Turno_final, '%d/%m/%Y %H:%M:%S'):
                #auxTemp1 = auxTemp2 = auxTemp3 = auxTemp4 = auxTemp5 = 0
                #status_slot1 = status_slot2 = status_slot3 = status_slot4 = status_slot5 = False
                lista_estado_puestos = [False for n in range(1,num_puestos + 1)]
                lista_auxTemp = [0 for n in range(1, num_puestos + 1)]
                data['parking_closed'] = True
            else:
                data['parking_closed'] = False
                Turno_inicio = str(now.day) +'/'+str(now.month) +'/'+str(now.year) +' 22:00:00'
                Turno_final = str(now.day + 1) +'/'+str(now.month) +'/'+str(now.year) +' 08:00:00'
                
                for i in range(0,len(lista_estado_puestos)):
                    if lista_auxTemp[i] == 0:
                        minutes = random.choice(rango)
                        lista_auxTemp[i] = now + timedelta(minutes=minutes)
                        lista_estado_puestos[i] = random.choice(slot_states)
                    elif now > lista_auxTemp[i]:
                        minutes = random.choice(rango)
                        lista_auxTemp[i] = now + timedelta(minutes=minutes)
                        lista_estado_puestos[i] = random.choice(slot_states)
                
                if getTimeWeather.hour == now.hour and getTimeWeather.minute == now.minute:
                    weather = mgr.weather_at_place('Montevideo,UY').weather
                    data['parking_temperature'] = weather.temperature(unit='celsius')['temp']
                    data['parking_humidity'] = weather.humidity
                    getTimeWeather = now + timedelta(minutes=30)
                else:
                    data['parking_temperature'] = weather.temperature(unit='celsius')['temp']
                    data['parking_humidity'] = weather.humidity

            data['device_timestamp'] = now.strftime('%Y-%m-%d %H:%M:%S')
            data['device_slots'] = []
            for i in range(0,len(lista_estado_puestos)):
                #data['slots'][i]['slot_id'] = str(i+1)
                data['device_slots'].append(lista_estado_puestos[i])
            
            # print(now.strftime('%Y-%m-%d %H:%M:%S')+" - "+str(data) + "\n")
            
            producer.send(topic, value=data)
            
            time.sleep(1)
        
        except Exception as e:
       	    ### Rutina de Devolución y Limpieza
            # activesDir = os.listdir(dirgeneral+parking+"/ActiveDevices")
            # if device+".txt" in activesDir:
            #     devices.append(device+"\n")
            with open(dirgeneral+parking+"/"+parking+"log.txt", "w") as f:
                f.write(e)
            with open(dirgeneral+parking+'/'+parking+'Devices.txt', 'a+') as f:
                f.write(device)
                f.write("\n")
            os.remove(dirgeneral+parking+"/ActiveDevices/"+device+".txt")
            activesDir = os.listdir(dirgeneral+parking+"/ActiveDevices")
            with open(dirgeneral+parking+'/AllActiveDevices.txt', 'w+') as f:
                dev2 = []
                for file in activesDir:
                    dev2.append(file.replace(".txt",""))
                f.writelines(dev2)
                f.write("\n")
            break

    
if __name__ == '__main__':
    main()
