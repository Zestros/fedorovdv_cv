import cv2
import zmq
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.morphology import binary_erosion

adress = "84.237.21.36"
port = 6002

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE,b"")
socket.connect(f"tcp://{adress}:{port}")

cv2.namedWindow("Client", cv2.WINDOW_GUI_NORMAL)
count = 0

while True:
    message = socket.recv()
    frame = cv2.imdecode(np.frombuffer(message, np.uint8),-1)
    count+=1
    blurred = cv2.GaussianBlur(frame,(11,11),0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(blurred, (0,0,0), (155,155,150))
    mask = np.invert(np.array(mask))
    mask_eroded = binary_erosion(mask, np.ones((35,35)))
    labeled = label(mask_eroded)
    regions = regionprops(labeled)
    c=0
    k=0
    for region in regions:
        if region.eccentricity>0.6:
            c+=1
        else:
            k+=1
    plt.imshow(mask_eroded)
    plt.show()
    print(f"Сейчас шариков {c}, а кубиков {k}" )
    key =chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break
    cv2.putText(frame, f"Count {count}", (10,60),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0))
    cv2.imshow("Client",mask)
