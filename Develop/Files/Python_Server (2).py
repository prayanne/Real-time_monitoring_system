'''echo_server1.py'''
import socket

import serial

import time

ser = serial.Serial("/dev/rfcomm1", 115200)
ser_wire = serial.Serial("/dev/ttyUSB0", 9600)

def run_server(msg_list, host="192.168.0.11", port=4000):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((host, port))
        s.listen(2)
        conn, addr = s.accept()
        conn.sendall(msg_list.encode())
        print("[", addr[0], "] is connected.\n>> The value is ", msg_list,"\n\n")
        conn.close()

if __name__ == '__main__':
    while 1:
        if ser.readable():  # 시리얼 통신이 이루어질 때, ser.readable()의 값이 1이 된다. 그러므로, if문이 실행됨.
             val = ser.readline()  # 변수 val에 수신된 값을 저장함. | ser = 시리얼 통신, .readline() = 파이썬에서 내용을 읽어올 때, 사용.
             val = val.decode('utf-8')[:len(val) - 2]  # val에 저장된 값을 utf-8로 디코딩함. | 아두이노와 파이썬의 문자 규격이 다르다.
             val_wire = ser_wire.readline()
             val_wire = val_wire.decode('utf-8')[:len(val_wire) - 2]
             val = val_wire + val
             val1 = val.split(',')  # 수신받은 문자열은 콤마(,)로 구분되고 있다. .split(',')은 문자열에서 콤마를 기준으로 분리해준다.
             print(val)
             #if int(val1[0]) == 0:  # val의 첫 번째 값, 오류 유무 코드가 0일 때, 정상 출력
             run_server(val)  # 수신된 후, 가공된 val 값을 불러옴. | 이 경우에는, [{0 or 1}, 습도값, 온도값]
