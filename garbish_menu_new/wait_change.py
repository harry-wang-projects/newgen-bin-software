import cv2
import numpy as np
from time import sleep

from camera_run import get_raw
from hardware_commands import get_weight

def get_action():
    #1. camera detection - check big changes in camera
    #2. weight detection - check big changes in weight
    gotten_image = get_raw()
    first_weight = get_weight() 
   
    sleep(0.3)

    #see if weight change big
    second_weight = get_weight()
    if(abs(second_weight - first_weight) > 3):
        return True

    second_image = get_raw()

    gotten_image = cv2.resize(gotten_image, (320, 240), interpolation = cv2.INTER_AREA)
    second_image = cv2.resize(second_image, (320, 240), interpolation = cv2.INTER_AREA)
    
    ##get difference
    diff = cv2.absdiff(gotten_image, second_image)

    ##grayscale and blur
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
       
    ##contour around areas
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    i = 0
    for c in contours:
        if cv2.contourArea(c) < 500:
            continue
        i += 1
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(second_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print("i count: ", i)
    if(i > 0):
         return True
    return False
     ##stop the program
#    if cv2.waitKey(10) == ord('q'):
#        return
 
#    cv2.imshow('test camera', second_image)

def wait_action():
    while True:
        if get_action() == True:
            break

sleep(5)
wait_action()
print("finished!")
