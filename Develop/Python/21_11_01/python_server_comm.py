'''Python_Server.py'''

# Writer: Writer
# Writing Date: 21/09/21
# Comment: A system of caring for patients. It is a real-time monitoring system.


#### Import Library ####
import socket
import threading
import time
import serial

#### Setting Global Variable ####
BPM = 0
SPO2 = 0
DHT = 0

######################################################################################################################

#### Setting Funtions ####


#### Main - Sensors Value output ####

## Use Socket Library [bind-listen-accept-sendall-close] ##

def run_server(msg_list, host="192.168.0.11", port=4000):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((host, port))
        s.listen(2)
        conn, addr = s.accept()
        conn.sendall(msg_list.encode())
        print("[", addr[0], "] is connected.\n>> The value is ", msg_list,"\n\n")
        conn.close()


#### Thread - Max30102 Value input ####

## Read Value -> Decode Data -> Input Decoded data to [Global Variable] - BPM and SPO2  ##

def thr_import_max():
    global BPM
    global SPO2

    while True:
        val_max_sum = 0
        count = 0
        for _ in range(10):
            val_max = ser_max.readline()
            val_max = val_max.decode('utf-8')[:len(val_max) - 2]
            val_max_split = val_max.split(",")
            try:
                if int(val_max_split[1]) is not 0:
                    bpm_value = val_max_split[1]
                if int(val_max_split[2]) > 80:
                    val_max_sum += int(val_max_split[2])
                    count += 1
            except ValueError:
                pass
        if count is not 0:
            val_max_avr = val_max_sum // count

        BPM = bpm_value
        SPO2 = str(val_max_avr)


#### Thread - DHT22 Value input ####

## Read Value -> Decode Data -> Input Decoded data to [Global Variable] - DHT  ##

def thr_import_dht():
    global DHT

    while True:
        val_dht = ser_dht.readline()
        val_dht = val_dht.decode('utf-8')[:len(val_dht) - 2]
        DHT = val_dht


#### Check and modify Datas ####

## Print Menu, [ Run Server | Print Sensors Values | Check Sensors Available ] ##

def checkValue():

    while True:
        valueType = int(input("\n0. Run Server\n1. DHT22 Value print\n2. Max30102 Value print\n3. DHT - Available Check\n4. Max30102 - Available Check\n5. All Value print\nCheck value type : "))
        if valueType == 1:
            val_dht = ser_dht.readline()
            val_dht = val_dht.decode('utf-8')[:len(val_dht) - 2]
            for _ in range(3):
                print(val_dht + "\n\n")

        elif valueType == 2:
            val_max_sum = 0
            val_max_avr = 0
            count = 0
            for _ in range(10):
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
            print(str(value_dht_available) + "\n\n")

        elif valueType == 4:
            value_max_available = ser_max.readable()
            print(str(value_max_available) + "\n\n")

        elif valueType == 5:
            val_dht = ser_dht.readline()
            val_dht = val_dht.decode('utf-8')[:len(val_dht) - 2]
            val_max = ser_max.readline()
            val_max = val_max.decode('utf-8')[:len(val_max) - 2]
            print(val_dht+val_max + "\n\n")

        elif valueType == 0:
            break

        else:
            print("plz again!")

#######################################################################################################################

#### Run Server ####


#### Pre-Funtion - Setting OS and Ports ####

## Select OS - Linux or Windows ##
## And Input Port number or Select Default Values ##

print("Select Serial Port Menu!\n")
while True:
    os_select = int(input("1. Linux\n2. Windows\n3. Linux Default\n4. Windows Default\nSelect your OS Menu: "))
    if os_select == 1:
        max_port = input("Enter Max30102 Port: /dev/rfcomm")
        tty_port = input("Enter DHT22 Port: /dev/ttyUSB")
        break
    elif os_select == 2:
        max_port = input("Enter Max30102 Port: COM")
        tty_port = input("Enter DHT22 Port: COM")
        break
    elif os_select == 3:
        max_port = input("Enter Max30102 Port: /dev/rfcomm")
        tty_port = 0
        break
    elif os_select == 4:
        max_port = 11
        tty_port = 15
        break
    else:
        print("Plz again")

## OS [Linux, Windows] Select And Input Values ##
if os_select == 1 or os_select == 3:
    ser_max = serial.Serial("/dev/rfcomm"+max_port, 115200)
    ser_dht = serial.Serial("/dev/ttyUSB"+tty_port, 9600)
elif os_select == 2 or os_select == 4:
    ser_max = serial.Serial("COM"+max_port, 115200)
    ser_dht = serial.Serial("COM"+tty_port, 9600)


#### Main Funtion - Check Values, Run Tread, Run Socket Server ####

if __name__ == '__main__':

    checkValue()

    dht_thr = threading.Thread(target=thr_import_dht)
    max_thr = threading.Thread(target=thr_import_max)

    dht_thr.start()
    max_thr.start()

    time.sleep(20)

    val = DHT + "," + str(BPM) + "," + str(SPO2)
    print("\n\nReady to connect.\n>>> " + val)

    while 1:
        val = DHT + "," + str(BPM) + "," + str(SPO2)
        run_server(val)
