'''echo_server1.py'''
import serial

import time

serial_sensor = serial.Serial("COM8", 9600)

def sensor_input():
    if serial_sensor.readable():  # 시리얼 통신이 이루어질 때, ser.readable()의 값이 1이 된다. 그러므로, if문이 실행됨.
        val = serial_sensor.readline()  # 변수 val에 수신된 값을 저장함. | ser = 시리얼 통신, .readline() = 파이썬에서 내용을 읽어올 때, 사용.
        val = val.decode('utf-8')[:len(val) - 2]  # val에 저장된 값을 utf-8로 디코딩함. | 아두이노와 파이썬의 문자 규격이 다르다.
        print(val)

if __name__ == '__main__':
    while 1:
         sensor_input()