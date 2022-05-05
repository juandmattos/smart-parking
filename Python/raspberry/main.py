from digi.xbee.devices import *
import re
import time

ALLDATA = {}
# Define callback.
def my_data_received_callback_from_arduino(xbee_message):
    # recepcion de la data
    address = xbee_message.remote_device.get_64bit_addr()
    data = xbee_message.data.decode("utf8")
    is_broadcast = xbee_message.is_broadcast
    timestamp = time.ctime(xbee_message.timestamp)
    print("Received data from {} with the next values {} ,  {} ,  {}".format(address, data, timestamp, is_broadcast))
    
    realDictData = {}
    # Parseo de la data    
    if len(data) == 30:
        LvlData2 = re.match(r'^(LVL\d)_ZN(\d)_T(\d+)H(\d+)(L[0-9])(\d)(L[0-9])(\d)(L[0-9])(\d)(L[0-9])(\d)(L[0-9])(\d)$', data)
        realDictData.update({LvlData2.group(1) : {
                                    LvlData2.group(5):LvlData2.group(6),
                                    LvlData2.group(7):LvlData2.group(8),
                                    LvlData2.group(9):LvlData2.group(10),
                                    LvlData2.group(11):LvlData2.group(12),
                                    LvlData2.group(13):LvlData2.group(14)
                                }, 'T': LvlData2.group(3),
                                    'H': LvlData2.group(4), 'timestamp': timestamp, 'XBEE': str(address), 'Zone': LvlData2.group(2)})
        
    print(realDictData)
        

    
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


