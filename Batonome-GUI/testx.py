import serial
import struct

ser = serial.Serial("COM4", baudrate=9600, timeout=1)

while True:
    data = "4"
    ser.write(data.encode())
    print("send 4")


    received_data = ser.read(    )
    if received_data:
        print(received_data)
        # format = '<ddfi'
        # # Décoder les données de la structure
        # double1, double2, float1, int1 = struct.unpack(format, received_data)    
        # print(double1)
        # print(double2)
        # print(float1)
        # print(int1)
        # received_data = 0
        # ser.flushInput()
        

ser.close()