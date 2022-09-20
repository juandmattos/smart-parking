#!/usr/bin/env python
# coding: utf-8
import random
import json
import time
import os
import sys
import pyowm
from kafka import KafkaProducer
from datetime import datetime, timedelta

# DIFERENTES RUTINAS DE ENTRADA Y DATOS NECESARIOS PARA SU USO


def getParameters(argv):
    try:
        opts, args = getopt.getopt(argv, "h:p:a:n:i:r", ["help", "description=", "address=", "name=", "id=", "create"])
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
    --parking (-p)\t\tParking Name (Mandatorio)
    --device (-a)\t\tNombre de la Calle y numero de puerta del Parking (Mandatorio)
    --num-puesto (-n)\t\tNombre del Parking (Mandatorio)
    --level (-l)\t\tID del parking(Mandatorio)
    --area-id (-i)\t\tFuncion de creacion del directorio del parking
    """)

def main():
    print("""


    
    Bienvenido al Tercer Script del Proyecto SmartParkingSystem,
    este script esta diseñado para la ejecución de un dispositivo virtual
    dentro de la red de estacionamientos en el sistema de BigData\n\n""")

    dirgeneral = "/opt/smart-parking/Python/Generator/Parkings/"
    directorios = os.listdir(dirgeneral)
    #create_opt, parking_description, parking_address, parking_name, parking_id = getParameters(sys.argv[1:]
    try:
        parking = sys.argv[1]
        if parking not in directorios:
            print("Entro1")
            exit()
    except IndexError:
        print("Indique en que Parking desea realizar la simulación: \n")
        for i in range(1, len(directorios)+1):
            print(str(i)+".- "+directorios[i-1])
        num = input("Ingrese su opción (1): ")
        parking = directorios[0] if num == "" else directorios[int(num) - 1]

    with open(dirgeneral+parking+'/'+parking+'Devices.txt', 'r') as f:
        devices = f.readlines()
        
    # FORMAT A JSON MODEL FOR PARKING
    with open(dirgeneral+parking+'/producer'+parking+'.json') as f:
        data = json.load(f)

    try:
        device = sys.argv[2]
        if device+"\n" not in devices:
            print("Entro2")
            exit()
        data['device_id'] = device
        devices.remove(device+"\n")
    except IndexError:
        print("\nSeleccione alguno de los siguientes dispositivos virtuales: ")
        for i in range(1, len(devices)+1):
            line = devices[i-1].replace("\n","")
            print(str(i)+".- "+line)
        num2 = input("Ingrese su opción (1): ")
        num2 = 1 if num2 == "" else int(num2)
        device = devices[num2-1].replace("\n", "")
        data['device_id'] = device
        devices.remove(devices[num2-1])

    with open(dirgeneral+parking+'/ActiveDevices/'+device+'.txt', 'w') as f:
        f.write("1\n")
        
    try:
        with open(dirgeneral+parking+'/AllActiveDevices.txt', 'a+') as f:
            f.write(device+"\n")
    except:
        with open(dirgeneral+parking+'/AllActiveDevices.txt', 'w+') as f:
            f.write(device)
            
    with open(dirgeneral+parking+'/'+parking+'Devices.txt', 'w') as f:
        f.writelines(devices)


    try:
        num_puestos = int(sys.argv[3])
    except IndexError:
        num_puestos = input("\nIndique cuantos puestos desea simular (10): ")
        num_puestos = 10 if num_puestos == "" else int(num_puestos)
    data['device_spots'] = str(num_puestos)


    for i in range(1,num_puestos + 1):
        data['device_slots'].append({})

    try:
        nivel = sys.argv[4]
    except IndexError:
        nivel = input("Indique el Nivel del estacionamiento (1): ")
        nivel = "1" if nivel == "" else nivel
    data['device_level_id'] = nivel 

    try:
        area = sys.argv[5]
    except IndexError:   
        area = input("Indique el numero de sector del estacionamiento (1): ")
        area = "1" if area == "" else area
    data['device_area_id'] = area 

    try:
        areaName = sys.argv[6]
    except IndexError:   
        areaName = input("Indique el nombre de sector del estacionamiento (A): ")
        areaName = "A" if areaName == "" else areaName  
    data['device_area_name'] = areaName

    # Values used to random function
    lista_estado_puestos = [False for n in range(1,num_puestos + 1)]
    lista_auxTemp = [0 for n in range(1, num_puestos + 1)]
    #rango = [2, 5, 10, 20, 30, 45, 60, 120, 240]
    rango = [1, 2]
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
        now = datetime.now()
        
        with open(dirgeneral+parking+'/ActiveDevices/'+device+'.txt', 'r') as f:
            status = f.readline()
        if status == '0\n':
            break
            
        if now >= datetime.strptime(Turno_inicio, '%d/%m/%Y %H:%M:%S') and now <= datetime.strptime(Turno_final, '%d/%m/%Y %H:%M:%S'):
            #auxTemp1 = auxTemp2 = auxTemp3 = auxTemp4 = auxTemp5 = 0
            #status_slot1 = status_slot2 = status_slot3 = status_slot4 = status_slot5 = False
            lista_estado_puestos = [False for n in range(1,num_puestos + 1)]
            lista_auxTemp = [0 for n in range(1, num_puestos + 1)]
        else:
            
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
        
        for i in range(0,len(lista_estado_puestos)):
            data['slots'][i]['slot_id'] = str(i+1)
            data['slots'][i]['state'] = lista_estado_puestos[i]
        
        # print(now.strftime('%Y-%m-%d %H:%M:%S')+" - "+str(data) + "\n")
        
        producer.send(topic, value=data)
        
        time.sleep(1)

    ### Rutina de Devolución y Limpieza
    # activesDir = os.listdir(dirgeneral+parking+"/ActiveDevices")
    # if device+".txt" in activesDir:
    #     devices.append(device+"\n")
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

    
if __name__ == '__main__':
    main()
