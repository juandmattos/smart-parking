import serial
from digi import XBeeDevice


# Instantiate a local XBee object.
xbee = XBeeDevice("/dev/ttyUSB0", 9600)
xbee.open()

# Read data.
xbee_message = xbee.read_data()

# serial_port = serial.Serial('/dev/ttyUSB0', 9600)
# xbee = XBee(serial_port)

# while True:
#     try:
#         print(xbee.wait_read_frame())
#     except KeyboardInterrupt:
#         break

# serial_port.close()
