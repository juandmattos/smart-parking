from digi.xbee.devices import *
import re
import json
import os
from kafka import KafkaProducer
from datetime import datetime, timedelta

ALLDATA = {}

# Initialize a Kafka Producer
PRODUCER = KafkaProducer(bootstrap_servers=['hadoop-namenode:9092'], api_version=(0,10,0), value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Define callback.
def my_data_received_callback_from_arduino(xbee_message):
    # recepcion de la data
    dirgeneral = "/home/pi/Documents/smart-parking/Python/raspberry"
    directorios = os.listdir(dirgeneral)
    # FORMAT A JSON MODEL FOR PARKING
    with open(dirgeneral+'/producerXBEE.json') as f:
        Json = json.load(f)
        
    address = xbee_message.remote_device.get_64bit_addr()
    Json['device_address'] = str(address)
    data = xbee_message.data.decode("utf8")
    is_broadcast = xbee_message.is_broadcast
    Json['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    num_puestos = 5    
    for i in range(1,num_puestos + 1):
        Json['slots'].append({})
    
    if len(data) == 30:
        LvlData2 = re.match(r'^(LVL\d)_ZN(\d)_T(\d+)H(\d+)(L[0-9])(\d)(L[0-9])(\d)(L[0-9])(\d)(L[0-9])(\d)(L[0-9])(\d)$', data)
        estadoPuestos = [LvlData2.group(6), LvlData2.group(8), LvlData2.group(10), LvlData2.group(12), LvlData2.group(14)]
        for i in range(0,num_puestos):
            Json['slots'][i]['slot_id'] = str(i+1)
            Json['slots'][i]['state'] = True if estadoPuestos[i] == "0" else False
        Json['temperature'] = LvlData2.group(3)
        Json['humidity'] = LvlData2.group(4)
    
    if '47A0E5' in str(address):
        Json['area_name'] = "A"
        topic = Json['parking_id']+"_"+Json['level_id']+"_"+Json['area_id']+"_"+Json['area_name'] 
        PRODUCER.send(topic, value=Json)
        print("Received data from {} with the next values {} ,  {} ,  {}".format(address, data, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), is_broadcast))
    elif '814D79' in str(address):
        Json['area_name'] = "B"
        topic = Json['parking_id']+"_"+Json['level_id']+"_"+Json['area_id']+"_"+Json['area_name'] 
        PRODUCER.send(topic, value=Json)
    
def main():
    print("Hello World!")
    # Retrieving the configured timeout for synchronous operations.
    print("Current timeout: %d seconds" % device.get_sync_ops_timeout())
    # Add the callback.
    while True:
        try:
            device.add_data_received_callback(my_data_received_callback_from_arduino)
        except Exception as e:
            print(e)

        device.del_data_received_callback(my_data_received_callback_from_arduino)

if __name__ == "__main__":
    # Instantiate an XBee device object.
    NEW_TIMEOUT_FOR_SYNC_OPERATIONS = 10 # 5 seconds
    
    device = XBeeDevice("/dev/ttyUSB0", 115200)
    # si se obtiene un error del estilo de no se puede obtener modo de operación es necesario 
    # realizar una apertura por serial o verificar que el puerto es parte del usuario pi 
    device.open()
    device.set_sync_ops_timeout(NEW_TIMEOUT_FOR_SYNC_OPERATIONS)
    main()
