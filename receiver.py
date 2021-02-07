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
background = None
### new
data = b""
payload_size = struct.calcsize("L") 
background_frames = 10
collected_bg = 0
has_background  = False
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
    image = frame
    key = cv2.waitKey(1)

    if background is None:
        background = np.zeros_like(image)

    if key == ord("s") :
        background = np.array(image.copy(), np.float)
        collected_bg=1
        has_background = False

    if collected_bg>0 and collected_bg<background_frames and not has_background:
    
        background+=np.array(image.copy(), np.float)
        collected_bg+=1

    elif collected_bg == background_frames and not has_background :
        background= background/collected_bg
        print(background.shape)
        background = np.array(background,np.uint8)
        
        has_background = True
    
    if has_background:
        image = image-background

        kernel = np.ones((5, 5), np.uint8) 
        boundaries = [
            ([10, 10, 10], [255,255,255])
        ]
        image[:,:,0] = cv2.erode(image[:,:,0], kernel)
        image[:,:,1] = cv2.erode(image[:,:,1], kernel)  
        image[:,:,2] = cv2.erode(image[:,:,2], kernel)  

        for (lower, upper) in boundaries:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")
            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(image, lower, upper)
            output = cv2.bitwise_and(image, image, mask = mask)
        image = output
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret,image = cv2.threshold(image,20,255,cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours)>0:
            cnt = max(contours, key = cv2.contourArea)

            cv2.drawContours(frame, [cnt], 0, (0,255,0), 3)
        
        cv2.imshow("frame",frame)
        #cv2.imshow("images", np.hstack([image[:,:,0],thresh]))
    else:
        cv2.imshow("frame",frame)

    
    duration = start_time-time.time()
