import socket

HOST = '10.0.0.14'  # The server's hostname or IP address
PORT = 4000        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    data = s.recv(2048)
    if not data:
        break
    print(repr(data))

