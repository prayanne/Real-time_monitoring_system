
import socket


def run_server(msg_list, host="192.168.0.11", port=4000):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((host, port))
        s.listen(2)
        conn, addr = s.accept()
        conn.sendall(msg_list.encode())
        print("[", addr[0], "] is connected.\n>> The value is ", msg_list,"\n\n")
        conn.close()



#######################################################################################################################

#### Run Server ####


#### Main Funtion - Check Values, Run Tread, Run Socket Server ####

if __name__ == '__main__':


    val = "0,65.00,25.00" + "," + "65" + "," + "98"
    print("\n\nReady to connect.\n>>> " + val)

    while True:
        for _ in range(4):
            val = "0,65.00,25.00" + "," + "65" + "," + "98"
            run_server(val)

        for _ in range(3):
            val = "0,65.00,25.00" + "," + "115" + "," + "98"
            run_server(val)

        for _ in range(3):
            val = "0,65.00,25.00" + "," + "50" + "," + "98"
            run_server(val)

        for _ in range(3):
            val = "0,65.00,25.00" + "," + "65" + "," + "70"
            run_server(val)