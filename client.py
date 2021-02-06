import socket
import cv2 as cv
import base64 as b64
import pickle
HOST = '10.0.0.14'  # The server's hostname or IP address
PORT = 4000        # The port used by the server


def recv(c):

    data = b""
    while True:
        block = c.recv(1024)
        print(block)
        if not block: 
            break
        data += block
    return data


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    data = recv(s)
    data = pickle.loads(data)


    print(data)
    
    cv.imshow("Frame", data["image"])
    key = cv.waitKey(1) & 0xFF

    if key == ord("q"):
        break

