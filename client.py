import socket
import cv2 as cv
import base64 as b64
import json
HOST = '10.0.0.14'  # The server's hostname or IP address
PORT = 4000        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    data = s.recv(2048).decode()
    data = json.loads(data)

    #data = b64.b64decode(data)
    if not data:
        break
    print(data)
    
    cv.imshow("Frame", data["image"])
    key = cv.waitKey(1) & 0xFF

    if key == ord("q"):
        break

