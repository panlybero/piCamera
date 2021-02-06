'''import socket
import cv2 as cv
import base64 as b64
import pickle
HOST = '10.0.0.14'  # The server's hostname or IP address
PORT = 4000        # The port used by the server


def recv(c):

    data = b""
    while True:
        block = c.recv(4096)
        #print(block)
        if not block: 
            break
        data += block
    return data


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    data = recv(s)
    print(len(data))
    data = pickle.loads(data)


    print(data)
    
    cv.imshow("Frame", data)
    key = cv.waitKey(1) & 0xFF

    if key == ord("q"):
        break

'''

from vidgear.gears import NetGear
import cv2

# define various tweak flags
options = {"flag": 0, "copy": False, "track": False}

# Define Netgear Client at given IP address and define parameters 
# !!! change following IP address '192.168.x.xxx' with yours !!!
client = NetGear(
    address="10.0.0.14",
    port="4000",receive_mode=True
)

# loop over
while True:

    # receive frames from network
    frame = client.recv()

    # check for received frame if Nonetype
    if frame is None:
        break

    # {do something with the frame here}

    # Show output window
    cv2.imshow("Output Frame", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close client
client.close()