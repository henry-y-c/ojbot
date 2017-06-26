import serial
ser = serial.Serial('/dev/cu.usbmodem1411', 115200)
while True:
    print(ser.readline())