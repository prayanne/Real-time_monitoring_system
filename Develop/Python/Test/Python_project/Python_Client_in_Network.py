'''echo_client1.py'''
import socket
def run(host='192.168.1.146', port=4000):
  with socket.socket() as s:
    s.connect((host, port))
    line = "Connected!"
    #s.sendall(line.encode())
    res_h = s.recv(1024)
    #res_t = s.recv(1024)
    print(f'={res_h.decode()}')
    #print(f'={res_t.decode()}')
if __name__ == '__main__':
  while 1:
    run()


"""
import socket

def client_socket(host='192.168.1.146', port=4000):
    with socket.socket() as sck:
        sck.connect((host, port))
        res = sck.recv(1024)
        print(res.decode())
        sck.sendall(res)
while 1:
    client_socket()
"""
