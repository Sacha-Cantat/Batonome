from digi.xbee.devices import XBeeDevice
device = XBeeDevice("COM4", 9600)

# 

device.open()

device.send_data_broadcast("Hello XBee!")
device.close()