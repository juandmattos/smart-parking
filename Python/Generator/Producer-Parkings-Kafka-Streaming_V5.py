#!/usr/bin/env python
# coding: utf-8
import argparse
import random
import json
import time
import os
import sys
import pyowm
from kafka import KafkaProducer
import holidays
from datetime import datetime, timedelta, date

# DIFERENTES RUTINAS DE ENTRADA Y DATOS NECESARIOS PARA SU USO
dirgeneral = "/opt/data/Generator/Parkings/"

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


def get_args():
    global dirgeneral
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--parking",
        help="Parking Name",
        choices=["PuntaCarretasShopping", "TresCrucesShopping"],
        required=True,
    )

    parser.add_argument(
        "-l",
        "--level-id",
        help="Parking Level-ID",
        dest="level_id",
        required=True,
    )

    parser.add_argument(
        "-ai",
        "--area-id",
        help="Parking Area-ID",
        dest="area_id",
        required=True,
    )

    parser.add_argument(
        "-an",
        "--area-name",
        help="Parking Area-Name",
        dest="area_name",
        required=True,
    )

    parser.add_argument(
        "-d",
        "--device",
        help="Device Name",
        dest="device",
        required=True,
    )

    parser.add_argument(
        "-q",
        "--qt-slots",
        help="Quantity of Slots on the Area",
        dest="qt_slots",
        required=True,
    )

    return parser.parse_args()


def main():
    print("""
    Bienvenido al Tercer Script del Proyecto SmartParkingSystem,
    este script esta diseñado para la ejecución de un dispositivo virtual
    dentro de la red de estacionamientos en el sistema de BigData\n\n""")

    # parking, device, num_puestos, nivel, area, areaName = getParameters(sys.argv[1:])
    # device = list_device[0]
    args = get_args()
    print(args)
    parking = args.parking
    num_puestos = int(args.qt_slots)
    device = args.device
    area = args.area_id
    areaName = args.area_name
    nivel = args.level_id

    # FORMAT A JSON MODEL FOR PARKING
    with open(dirgeneral+parking+'/producer'+parking+'.json') as f:
        data = json.load(f)

    # DEVICES OPTION
    with open(dirgeneral+parking+'/'+parking+'Devices.txt', 'r') as f:
        devices = f.readlines()
    device = random.choice(devices) if device == "" else device
    try:
        device = device.replace("\n", "")   
    except Exception as e:
        print(e)
    devices = [k.replace("\n","") for k in devices]
    if device not in devices:
        print("The device is not in the Parking Devices List... Please, Try Again!!")
        #getAvailabledevices(devices)
        sys.exit()
    
    if len(device) != 16:
        print("The device should have 16 length... Please, Try Again!!")
        #getAvailabledevices(devices)
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

    data['device_id'] = device
    data['device_spots'] = str(num_puestos)
    data['device_level_id'] = nivel 
    data['device_area_id'] = area 
    data['device_area_name'] = areaName

    # Values used to random function
    lista_estado_puestos = [False for n in range(1,num_puestos + 1)]
    lista_auxTemp = [0 for n in range(1, num_puestos + 1)]
    rango = [2, 3, 5, 7, 8, 10, 12, 15, 20, 25, 30, 45, 60, 90, 115, 120, 240]
    #rango = [1, 2]
    slot_states = [True, False]

    # Rangos de fechas para horario nocturno, en el cual los carros se encuentran dentro del Parking
    Turno_inicio = str(datetime.now().day) +'/'+str(datetime.now().month) +'/'+str(datetime.now().year) +' 22:00:00'
    Turno_final = str(datetime.now().day + 1) +'/'+str(datetime.now().month) +'/'+str(datetime.now().year) +' 08:00:00'

    # Obtener fecha de primera consulta para el tiempo
    APIKEY='055bcf46839359ea922b925c3d7cd860'        # your API Key here as string
    #APIKEY='80237b0c490766db2b30a55e03099d4e'
    owm = pyowm.OWM(APIKEY)                       # Use API key to get data
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place('Montevideo,UY').weather
    getTimeWeather = datetime.now() + timedelta(minutes=30)
    data['parking_temperature'] = weather.temperature(unit='celsius')['temp']
    data['parking_humidity'] = weather.humidity
    data['parking_weather_status'] = weather.status
    data['parking_weather_status_detailed'] = weather.detailed_status
    data['parking_wind_speed'] = weather.wind()['speed']

    data['device_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Initialize a Kafka Producer
    producer = KafkaProducer(bootstrap_servers=['hadoop-namenode:9092'], api_version=(0,10,0), value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    topic = data['parking_name']
    print("El Topico a consumir es - "+topic)

    #Get Holidays
    dataHolidaysDict = holidays.Uruguay(years = [2022, 2023])
    feriadosLaborales = []
    feriadosNoLaborales = []
    for day, descrip in dataHolidaysDict.items():
        if ("01-01" in datetime.strftime(day, '%d-%m-%Y') or
            "01-05" in datetime.strftime(day, '%d-%m-%Y') or
            "18-07" in datetime.strftime(day, '%d-%m-%Y') or 
            "25-12" in datetime.strftime(day, '%d-%m-%Y') or 
            "25-08" in datetime.strftime(day, '%d-%m-%Y')):
            
            feriadosNoLaborales.append(day)
            #print(day, descrip, "Feriado No Laborable")
        else:
            feriadosLaborales.append(day)
            #print(day, descrip, "Feriado Laborable")
    today = datetime.now()


    # LOOP PARA ENVIAR DATOS A KAFKA
    while True:
        try:
            now = datetime.now()
            #print("NOW - " + str(now))
            if today.day == now.day:
                auxDate = date(now.year, now.month, now.day)
                if auxDate in feriadosLaborales:
                    data['parking_holiday_status'] = True
                    data['parking_holiday_description'] = dataHolidaysDict[auxDate]
                    data['parking_holiday_type'] = "L"
                elif auxDate in feriadosNoLaborales:
                    data['parking_holiday_status'] = True
                    data['parking_holiday_description'] = dataHolidaysDict[auxDate]
                    data['parking_holiday_type'] = "NL"
                else:
                    data['parking_holiday_status'] = False
                    data['parking_holiday_description'] = None
                    data['parking_holiday_type'] = "L"
                today = today + timedelta(days=1)

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
                    data['parking_weather_status'] = weather.status
                    data['parking_weather_status_detailed'] = weather.detailed_status
                    data['parking_wind_speed'] = weather.wind()['speed']

                    getTimeWeather = now + timedelta(minutes=2)
                else:
                    data['parking_temperature'] = weather.temperature(unit='celsius')['temp']
                    data['parking_humidity'] = weather.humidity
                    data['parking_weather_status'] = weather.status
                    data['parking_weather_status_detailed'] = weather.detailed_status
                    data['parking_wind_speed'] = weather.wind()['speed']


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
