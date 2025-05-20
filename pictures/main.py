import cv2
import numpy as np
from skimage.measure import label, regionprops
import os
import matplotlib.pyplot as plt
#165

video_path = 'output.avi'
capture = cv2.VideoCapture(video_path)

#save_dir = 'detected_frames1'
#os.makedirs(save_dir, exist_ok=True)

cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
c=0
i=0
print("Всего кадров в видео: ",capture.get(cv2.CAP_PROP_FRAME_COUNT))
while True:
    ret, frame = capture.read()
    if not(ret):
        break
    i+=1


    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    frame = cv2.threshold(frame, 224, 255, cv2.THRESH_BINARY_INV)[1]

    kernel = np.ones((5, 5), np.uint8)
    frame = cv2.erode(frame, kernel, iterations=2)

    #filename = f"{save_dir}/img_{i}.png"
    #cv2.imwrite(filename, frame)
    labelled = label(frame)
    regions = regionprops(labelled)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if len(regions)==1:
        ecc = regions[0].eccentricity
        area = regions[0].area
        if 0.3<ecc<0.5 and area > 1000:

            #labelled_filename = f"{save_dir}/{len(regions)}_{i}.png"
            #plt.imsave(labelled_filename, labelled, cmap='viridis')
            cv2.imshow("Frame", frame)
            c=c+1

print(c)
capture.release()
cv2.destroyAllWindows()



