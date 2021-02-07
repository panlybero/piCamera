import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import time
HOST=''
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('Socket created')

s.bind((HOST,PORT))
print ('Socket bind complete')
s.listen(10)
print ('Socket now listening')

conn,addr=s.accept()

### new
data = b""
payload_size = struct.calcsize("L") 
while True:
    start_time = time.time()
    while len(data) < payload_size:
        data += conn.recv(4096)
        
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    ###

    frame=pickle.loads(frame_data)
    #print(frame)
    #cv2.imshow('frame',frame)
    '''
    boundaries = [
    ([17, 15, 100], [50, 56, 200]),
    ([86, 31, 4], [220, 88, 50]),
    ([25, 146, 190], [62, 174, 250]),
    ([103, 86, 65], [145, 133, 128])
    ]
    '''
    boundaries = [
    ([60, 60, 60], [255, 255, 255]),
    
    ]

    
    image = frame
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)
        # show the images
        cv2.imshow("images", np.hstack([image[:,:,0], mask]))
        cv2.waitKey(1)
    
    duration = start_time-time.time()
