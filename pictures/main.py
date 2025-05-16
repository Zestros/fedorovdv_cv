import cv2
import numpy as np
from skimage.measure import label, regionprops
import os
#165

video_path = 'output.avi'
capture = cv2.VideoCapture(video_path)


cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
c=0

while True:
    ret, frame = capture.read()
    if not(ret):
        break

    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    frame = cv2.threshold(frame, 224, 255, cv2.THRESH_BINARY)[1]

    labelled = label(frame)
    regions = regionprops(labelled)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if len(regions)==1:
        ecc = regions[0].eccentricity
        if 0.7<ecc<0.8:
            cv2.imshow("Frame", frame)
            c=c+1

print(c)     
cv2.destroyAllWindows()
