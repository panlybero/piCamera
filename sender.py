import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('10.0.0.159',8089))
while True:
    ret,frame=cap.read()
    frame = cv2.resize(frame, (int(frame.shape[0]/2),int(frame.shape[1]/2))
    data = pickle.dumps(frame) ### new code
    clientsocket.sendall(struct.pack("L", len(data))+data) ### new code