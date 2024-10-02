'''echo_server1.py'''
import socket

import serial

import threading

import time

#### Check and modify Datas ####

print("Serial Port!\nDefault value is ")

BPM = 0
SPO2 = 0
DHT = 0

#ser_max = serial.Serial("/dev/rfcomm1", 115200)
#ser_dht = serial.Serial("/dev/ttyUSB0", 9600)
ser_max = serial.Serial("COM11", 115200)
ser_dht = serial.Serial("COM15", 9600)

def run_server(msg_list, host="192.168.1.146", port=4000):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((host, port))
        s.listen(2)
        conn, addr = s.accept()
        conn.sendall(msg_list.encode())
        print("[", addr[0], "] is connected.\n>> The value is ", msg_list,"\n\n")
        conn.close()


def thr_import_max():
    while True:
        global BPM
        global SPO2
        val_max_sum = 0
        count = 0
        for i in range(10):
            val_max = ser_max.readline()
            val_max = val_max.decode('utf-8')[:len(val_max) - 2]
            val_max_split = val_max.split(",")
            if int(val_max_split[1]) is not 0:
                BPM_value = val_max_split[1]
            if int(val_max_split[2]) > 80:
                val_max_sum += int(val_max_split[2])
                count += 1
        if count is not 0:
            val_max_avr = val_max_sum // count

        BPM = BPM_value
        SPO2 = str(val_max_avr)


def thr_import_dht():
    while True:
        global DHT
        val_dht = ser_dht.readline()
        val_dht = val_dht.decode('utf-8')[:len(val_dht) - 2]
        DHT = val_dht


def checkValue():

    while True:
        valueType = int(input("1. DHT22 Value print\n2. Max30102 Value print\n3. DHT - Available Check\n4.Max30102 - Available Check\n5. All Value print\nCheck value type : "))
        if valueType == 1:
            val_dht = ser_dht.readline()
            val_dht = val_dht.decode('utf-8')[:len(val_dht) - 2]
            for i in range(3):
                print(val_dht + "\n\n")

        elif valueType == 2:
            val_max_sum = 0
            val_max_avr = 0
            count = 0
            for i in range(10):
                val_max = ser_max.readline()
                val_max = val_max.decode('utf-8')[:len(val_max) - 2]
                val_max_split = val_max.split(",")
                if int(val_max_split[2]) > 80:
                    val_max_sum += int(val_max_split[2])
                    count += 1
                print(val_max)
            if count is not 0:
                val_max_avr = val_max_sum // count
            print("\n" + val_max_split[1] + "," + str(val_max_avr) + "\n\n")

        elif valueType == 3:
            value_dht_available = ser_dht.readable()
            print(value_dht_available + "\n\n")
            #if value_dht_available == 0:
            #    print("")

        elif valueType == 4:
            value_max_available = ser_max.readable()
            print(value_max_available + "\n\n")


        elif valueType == 5:
            val_dht = ser_dht.readline()
            val_dht = val_dht.decode('utf-8')[:len(val_dht) - 2]
            val_max = ser_max.readline()
            val_max = val_max.decode('utf-8')[:len(val_max) - 2]
            print(val_dht+val_max + "\n\n")

        elif valueType == 0:
            break


if __name__ == '__main__':

    checkValue()

    dht_thr = threading.Thread(target=thr_import_dht)
    max_thr = threading.Thread(target=thr_import_max)

    dht_thr.start()
    max_thr.start()

    time.sleep(20)

    val = DHT + "," + str(BPM) + "," + str(SPO2)
    print("Ready to connect.\n >>> " + val)

    while 1:
        val = DHT + "," + str(BPM) + "," + str(SPO2)
        run_server(val)

        """
        if ser_max.readable():  # 시리얼 통신이 이루어질 때, ser.readable()의 값이 1이 된다. 그러므로, if문이 실행됨.
             val_max = ser_max.readline()  # 변수 val에 수신된 값을 저장함. | ser = 시리얼 통신, .readline() = 파이썬에서 내용을 읽어올 때, 사용.
             val_max = val_max.decode('utf-8')[:len(val_max) - 2]  # val에 저장된 값을 utf-8로 디코딩함. | 아두이노와 파이썬의 문자 규격이 다르다.
             val_dht = ser_dht.readline()
             val_dht = val_dht.decode('utf-8')[:len(val_dht) - 2]
             val = val_dht + val_max
             val_split = val.split(',')  # 수신받은 문자열은 콤마(,)로 구분되고 있다. .split(',')은 문자열에서 콤마를 기준으로 분리해준다.
             print(val)
             #if int(val_split[0]) == 0:  # val의 첫 번째 값, 오류 유무 코드가 0일 때, 정상 출력
             run_server(val)  # 수신된 후, 가공된 val 값을 불러옴. | 이 경우에는, [{0 or 1}, 습도값, 온도값]
"""