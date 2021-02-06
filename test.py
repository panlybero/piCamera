# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import socket
import pickle
import sys
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)

HOST = '10.0.0.14'  # Standard loopback interface address (localhost)
PORT = "4000"        # Port to listen on (non-privileged ports are > 1023)
'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()

        

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    
    image = frame.array
    image = np.array(image)
    
    data = pickle.dumps(image)
   
    conn.sendall(data)
    
    rawCapture.truncate(0)
	
'''
from vidgear.gears import VideoGear
from vidgear.gears import NetGear

server = NetGear(address = HOST, port = PORT) #Define netgear server with default settings

# infinite loop until [Ctrl+C] is pressed
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    try: 
        image = frame.array
        image = np.array(image)
        
        
        
        
        frame = image
        # read frames

        # check if frame is None
        if frame is None:
            #if True break the infinite loop
            break

        # do something with frame here

        # send frame to server
        server.send(frame)
        rawCapture.truncate(0)
    
    except KeyboardInterrupt:
        #break the infinite loop
        break

# safely close video stream
stream.stop()
# safely close server
writer.close()