import serial
import time

ser = serial.Serial('COM11', 9600)

while True:
    if ser.readable():
        val = input()
        val = val.encode('utf-8')
        ser.write(val)

"""
        val = input()
        if val == '1':
            val = val.encode('utf-8')
            ser.write(val)
            print("LED TURNED ON")
            time.sleep(0.5)

        elif val == '0':
            val = val.encode('utf-8')
            ser.write(val)
            print("LED TURNED OFF")
            time.sleep(0.5)
            """
