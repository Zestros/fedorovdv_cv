from skimage.measure import label, regionprops
import time
import mss
import cv2
import numpy as np
import pyautogui
import math

def get_browser_window_size():
    screen_width, screen_height = pyautogui.size()
    return screen_width, screen_height

def capture_game_field():
    screen_width, screen_height = get_browser_window_size()
    

    GAME_WIDTH_PERCENTAGE = 0.3
    GAME_HEIGHT_PERCENTAGE = 0.08
    

    game_top = 305 #int(screen_height * 0.15)
    game_left = 695 #int((screen_width - screen_width * GAME_WIDTH_PERCENTAGE) / 2)
    game_width = 430 #int(screen_width * GAME_WIDTH_PERCENTAGE)
    game_height = 45 #int(screen_height * GAME_HEIGHT_PERCENTAGE)

    #with mss.mss() as sct:
    monitor = {"top": game_top,
                   "left": game_left,
                   "width": game_width,
                   "height": game_height}
        #screenshot = sct.grab(monitor)
        #arr = np.array(screenshot)
        #rgb_arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2RGB)
        #cv2.imshow("Game Field", rgb_arr)
        #cv2.waitKey(1)
    return monitor
sle =0.3

def detect_and_jump(game_monitor):
    screen_width, screen_height = get_browser_window_size()
    

    DETECT_WIDTH_RATIO = 0.3
    DETECT_HEIGHT_RATIO = 0.2      
    

    base_width = int(game_monitor['width'] * DETECT_WIDTH_RATIO)
    base_height = int(game_monitor['height'] * DETECT_HEIGHT_RATIO)
    

    start_top = game_monitor['top'] + int(game_monitor['height'] * 0.6)
    start_left = game_monitor['left'] + int(game_monitor['width'] * 0.1)
 
    start_time_game = time.time()
    last_jump_time = 0
    down_pressed = False  
    object_detected = False
    sum_y = 0.001
    n_y = 1
    
    with mss.mss() as sct:
        while True:
            current_time = time.time()
            game_time = current_time - start_time_game
            monitor = {
                "top": start_top,
                "left": start_left,
                "width": base_width,
                "height": base_height
            }
            img = sct.grab(monitor)
            img_np = np.array(img)
            hsv_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2HSV)

            lower_grey = np.array([0, 0, 50])
            upper_grey = np.array([180, 50, 150])
            
            mask = cv2.inRange(hsv_img, lower_grey, upper_grey)
            kernel = np.ones((3, 3), np.uint8)
            cleaned_mask = cv2.erode(mask, kernel, iterations=1)
            cleaned_mask = cv2.dilate(cleaned_mask, kernel, iterations=1)
            labeled = label(cleaned_mask)
            regions = regionprops(labeled)
            for region in regions:
                y, x = region.centroid
                #print(y)
                distance_to_edge = x
                if game_time > 40:
                    if distance_to_edge < base_width * 0.5:
                        if 2.9 >y:
                            correct_fly(3)
                        elif game_time > 15:
                            correct_fly(1)
                        elif game_time > 25:
                            correct_fly(4)
                        else:
                            correct_fly()
                        break
                elif game_time > 70:
                    sle=0.2
                    if distance_to_edge < base_width * 0.7:
                        if 2.9 >y:
                            correct_fly(3)
                        elif game_time > 15:
                            correct_fly(1)
                        elif game_time > 25:
                            correct_fly(4)
                        else:
                            correct_fly()
                        break
                else:
                    if distance_to_edge < base_width * 0.3:
                        if 2.9 >y:
                            correct_fly(3)
                        elif game_time > 15:
                            correct_fly(1)
                        elif game_time > 25:
                            correct_fly(2)
                        else:
                            correct_fly()
                        break
    
def correct_fly(fly_type = 0):
    if fly_type == 0:
        pyautogui.press('space')
    if fly_type == 1:
        pyautogui.press('space')
        time.sleep(0.1)
        pyautogui.press('down')
    if fly_type == 2:
        pyautogui.press('space')
        time.sleep(0.01)
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
    if fly_type == 3:
        pyautogui.keyDown('down')
        time.sleep(sle)
        pyautogui.keyUp('down')
    if fly_type == 4:
        pyautogui.press('space')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
    return

input("Start")

game_monitor = capture_game_field()
detect_and_jump(game_monitor)
