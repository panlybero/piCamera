# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

import socket

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 4000        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()

        

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    rawCapture.truncate(0)
    image = frame.array
    image = np.array(image)
    print(image.shape)
    conn.sendall(image)
	