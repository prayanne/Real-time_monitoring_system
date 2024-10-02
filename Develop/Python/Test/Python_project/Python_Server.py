'''echo_server1.py'''
import socket

import serial

import time

ser = serial.Serial("COM11",9600)

def run_server(msg_h, msg_t, host="192.168.1.146", port=4000):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(2)
        conn, addr = s.accept()
        #msg = conn.recv(1024)
        #print(f'{msg.decode()}')
        conn.sendall(msg_h.encode())
        #conn.sendall(msg_t.encode())
        #time.sleep(1)
        conn.close()

if __name__ == '__main__':

  while 1:
      if ser.readable():  # 시리얼 통신이 이루어질 때, ser.readable()의 값이 1이 된다. 그러므로, if문이 실행됨.
          val = ser.readline()  # 변수 val에 수신된 값을 저장함. | ser = 시리얼 통신, .readline() = 파이썬에서 내용을 읽어올 때, 사용.
          val = val.decode('utf-8')[:len(val) - 2]  # val에 저장된 값을 utf-8로 디코딩함. | 아두이노와 파이썬의 문자 규격이 다르다.
          val = val.split(',')  # 수신받은 문자열은 콤마(,)로 구분되고 있다. .split(',')은 문자열에서 콤마를 기준으로 분리해준다.
          if int(val[0]) == 0:  # val의 첫 번째 값, 오류 유무 코드가 0일 때, 정상 출력
            print(val)
            print(str(val[1]))
            print(str(val[2]))
            run_server(str(val[1]), str(val[2]))  # 수신된 후, 가공된 val 값을 불러옴. | 이 경우에는, [{0 or 1}, 습도값, 온도값]
          elif int(val[0]) == 1:  # val의 첫 번째 값, 오류 유무 코드가 1일 때, 오류문 출력
            print("DHT22 has Error!")  # 오류 출력문



"""
'''echo_server1.py'''
import socket

import serial #라이브러리인 Pyserial, import는 serial로 호출한다.

ser = serial.Serial('COM6', 9600) #시리얼 통신을 위한 준비작업 | (포트, 통신 비트레이트)
#변수 ser 이 시리얼 통신의 주가 된다.


def run_server(msg, host="192.168.1.161", port=4000):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()
        msg = conn.recv(1024)
        print(f'{msg.decode()}')
        conn.sendall(msg)
        conn.close()

if __name__ == '__main__':
    while 1:
        if ser.readable():  # 시리얼 통신이 이루어질 때, ser.readable()의 값이 1이 된다. 그러므로, if문이 실행됨.
            val = ser.readline()  # 변수 val에 수신된 값을 저장함. | ser = 시리얼 통신, .readline() = 파이썬에서 내용을 읽어올 때, 사용.
            val = val.decode('utf-8')[:len(val) - 2]  # val에 저장된 값을 utf-8로 디코딩함. | 아두이노와 파이썬의 문자 규격이 다르다.
            val = val.split(',')  # 수신받은 문자열은 콤마(,)로 구분되고 있다. .split(',')은 문자열에서 콤마를 기준으로 분리해준다.
            if int(val[0]) == 0:  # val의 첫 번째 값, 오류 유무 코드가 0일 때, 정상 출력
                run_server(val, host="127.0.0.1", port=4000)  # 수신된 후, 가공된 val 값을 불러옴. | 이 경우에는, [{0 or 1}, 습도값, 온도값]
            elif int(val[0]) == 1:  # val의 첫 번째 값, 오류 유무 코드가 1일 때, 오류문 출력
                print("DHT22 has Error!")  # 오류 출력문

"""


"""
import socket
BUF_SIZE = 1024
msg =""

def run_server(host="127.0.0.1", port=4000):
    with socket.socket() as sck:

        sck.bind((host, port))
        sck.listen(1)
        print("Connected!")
        conn, addr = sck.accept()
        #msg = 
        sck.sendall(msg.encode())
        #print("Enter msg is "+msg.decode())
        print("Receive msg is " + conn.recv(BUF_SIZE).decode())
        conn.close()
if __name__ == '__main__':
    while 1:
        print("Enter a message!")
        msg = input("> ")
        run_server(host="127.0.0.1", port=4000)
"""
