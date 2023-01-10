import serial

ser = serial.Serial("COM4", baudrate=9600, timeout=1)

while True:
    # data = "Hi"
    # ser.write(data.encode())

    received_data = ser.readline().decode()
    if received_data:
        print("Received data: ", received_data)
        

ser.close()