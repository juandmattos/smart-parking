import os 
import string
import random

directorios = os.listdir("/opt/smart-parking/Python/Generator/Parkings")
op = 0
print("###########################################################")
print("##                                                       ##")
print("##                     MENU GENERADOR                    ##")
print("##                                                       ##")
print("###########################################################\n")
print("OPCIONES:")
print("1.- Ejecucion para todos los parkings")
print("2.- Ejecucion para un parking en especifico")
print("9.- Salir")

op = input("Indique su opcion (1): ")
op = 1 if op == "" else int(op)

# print("Indique el número sobre que Parking desea realizar la simulación: \n")
# for i in range(1, len(directorios)+1):
#     print(str(i)+".- "+directorios[i-1])
# num = input("Ingrese su opción (1): ")
# parking = directorios[0] if num == "" else directorios[int(num) - 1]
    
if op == 1:
    length_of_string = 16
    number_of_strings = input("Indique cantidad de dispositivos a generar (10): ")
    number_of_strings = 10 if number_of_strings == "" else int(number_of_strings)

    devicesFinal = {}
    for d in directorios:
        devices = []
        for x in range(number_of_strings):
            devices.append(''.join(random.choice(string.ascii_uppercase[0:6] + string.digits) for _ in range(length_of_string)))
        devicesFinal[d] = devices
        
        with open("/opt/smart-parking/Python/Generator/Parkings/"+d+"/"+d+"Devices.txt", "w+") as f:
            f.write("\n".join(devicesFinal[d]))
            f.write("\n")
elif op == 2:
    length_of_string = 16
    
    print("Indique el número del Parking que desea realizar la creacion: \n")
    for i in range(1, len(directorios)+1):
        print(str(i)+".- "+directorios[i-1])
    num = input("Ingrese su opción (1): ")
    parking = directorios[0] if num == "" else directorios[int(num) - 1]
    
    number_of_strings = input("Indique cantidad de dispositivos a generar (10): ")
    number_of_strings = 10 if number_of_strings == "" else int(number_of_strings)

    devices = []
    for x in range(number_of_strings):
        devices.append(''.join(random.choice(string.ascii_uppercase[0:6] + string.digits) for _ in range(length_of_string)))
    
    with open("/opt/smart-parking/Python/Generator/Parkings/"+parking+"/"+parking+"Devices.txt", "w+") as f:
        f.write("\n".join(devices))
        f.write("\n")
elif op == 9:
    print("FIN DE EJECUCION...")
else:
    print("SELECCIONO UNA OPCION INVALIDA...")