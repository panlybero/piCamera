import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('10.0.0.159',8089))
scale_factor = 0.25
while True:
    ret,frame=cap.read()
    frame = cv2.resize(frame, (int(frame.shape[0]*scale_factor),int(frame.shape[1]*scale_factor)))
    data = pickle.dumps(frame) ### new code
    clientsocket.sendall(struct.pack("L", len(data))+data) ### new code