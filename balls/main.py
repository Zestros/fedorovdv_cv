import cv2
import numpy as np
import time
import json
import os
import random

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE,3)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
capture.set(cv2.CAP_PROP_EXPOSURE,-2)


def get_color(image):
    x, y, w, h = cv2.selectROI("Color selection", image)
    roi = image[y:y+h,x:x+w]
    color = (np.median(roi[:,:,0]),np.median(roi[:,:,1]),np.median(roi[:,:,2]))
    cv2.destroyWindow("Color selection")
    return color

def get_ball(image, color):
    lower = (np.max(color[0]-5,0), color[1]*0.8, color[2]*0.8)
    upper = (color[0]+5, 255, 255)
    mask = cv2.inRange(image, lower, upper)
    mask = cv2.erode(mask,None,iterations=2)
    mask = cv2.dilate(mask,None,iterations=2)
    contours, _ = cv2.findContours(mask,
                                   cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours)>0:
        contour = max(contours, key = cv2.contourArea)
        (x,y), radius = cv2.minEnclosingCircle(contour)
        x = int(x)
        y = int(y)
        radius = int(radius)
        return True, (x,y,radius, mask)
    return False, (-1,-1,-1,np.array(([])))

path = "settings.json"
if os.path.exists(path):
    base_colors = json.load(open(path,"r"))
else:
    base_colors = {}

game_started = False
guess_colors = []

dict_x ={}
while capture.isOpened():
    ret, frame = capture.read()
    blurred = cv2.GaussianBlur(frame,(11,11),0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    key = cv2.waitKey(1) & 0xFF
    if chr(key)=='q':
        break
    if chr(key)=='1':
        color = get_color(hsv)
        base_colors["1"] = color
    if chr(key)=='2':
        color = get_color(hsv)
        base_colors["2"] = color
    if chr(key)=='3':
        color = get_color(hsv)
        base_colors["3"] = color
    #if chr(key)=='4':
     #   color = get_color(hsv)
      #  base_colors["4"] = color
    for key in base_colors:
        retr, (x, y, radius, mask) = get_ball(hsv, base_colors[key])
        if retr:
            #cv2.imshow("Mask", mask)
            cv2.circle(frame, (x,y), radius,(255,0,255),2)
            if game_started:
                cv2.putText(frame, f"Game win = {guess_colors}",
                            (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (255,0,255))
                if key == "1":
                    dict_x[key] = x#+y
                if key == "2":
                    dict_x[key] = x#+y
                if key == "3":
                    dict_x[key] = x#+y
                #if key == "4":
                 #   dict_x[key] = x+y
    sort_dict_x = sorted(dict_x.items(), key=lambda item: item[1])
    if len(sort_dict_x) == 3:
        if sort_dict_x[0][0] == guess_colors[0] and sort_dict_x[1][0] == guess_colors[1] and sort_dict_x[2][0] == guess_colors[2]:
            print("Win")
            random.shuffle(guess_colors)
                    
    if len(base_colors) == 3:
        if not game_started:
            guess_colors = list(base_colors)
            random.shuffle(guess_colors)
            game_started = True
    cv2.putText(frame, f"Game started = {game_started}", (10,20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255))
    cv2.imshow("Camera", frame)
    


capture.release() 
cv2.destroyAllWindows()
json.dump(base_colors, open(path, "w"))
