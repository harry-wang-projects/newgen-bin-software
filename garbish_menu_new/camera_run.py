import cv2
import numpy as np
import os
import requests
import json
import pickle
import base64

from time import sleep

from classification_specs import IMG_SIZE, number_of_colors 
from hardware_commands import get_button

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

camera = cv2.VideoCapture(0)

def set_default(obj):
    print('type of final:', type(obj))
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def send_image(tosend):
    print(type(tosend))
    url = 'https://recycling.student.isf.edu.hk:81/nggetcamera'

    tosend = ({'picturearray': base64.b64encode(tosend).decode('ascii')})
    print(tosend)
    x = requests.post(url, json = tosend, verify = False)
    print("results")
    print(x.content)

    decoded_thing = json.loads(x.content)
    
    return decoded_thing["class"]

def get_pic():
    while not camera.isOpened():
        sleep(0.01)
#      if number_of_colors == 1:
#          img_array = cv2.imread(1, cv2.IMREAD_GRAYSCALE)  # read in the image, convert to grayscale
#    else:
#        img_array = cv2.imread(1)
    return_value, img_array = camera.read()
    print(return_value)
    print(img_array)

    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE), interpolation = cv2.INTER_AREA)

    #cv2.imshow("asdf", new_array)
    #cv2.waitKey(1000)

    new_array = np.asarray(new_array, dtype=np.float32).reshape(1, 224, 224, 3)


    new_array = (new_array / 127.5) - 1

    print(new_array)
    print(new_array.shape)

    pickle_data = pickle.dumps(new_array)
    print('pickle type: ', type(pickle_data))

    camresult = send_image(pickle_data)

    return camresult, new_array

def get_pic_array():
    while not camera.isOpened():
        sleep(0.01)
#      if number_of_colors == 1:
#          img_array = cv2.imread(1, cv2.IMREAD_GRAYSCALE)  # read in the image, convert to grayscale
#    else:
#        img_array = cv2.imread(1)
    return_value, img_array = camera.read()
    #print(return_value)
    #print(img_array)

    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE), interpolation = cv2.INTER_AREA)

    cv2.imshow("asdf", new_array)
    cv2.waitKey(1000)

    new_array = np.asarray(new_array, dtype=np.float32).reshape(1, 224, 224, 3)


    new_array = (new_array / 127.5) - 1


    return pickle.dumps(new_array)

def verify_classes(name, manual):
    img = np.empty((1, 224, 224 ,3))
    if manual:
        value = get_button()
        print("value:", value)
        if value == 0:
            return False, img
        else:
            return True, img


    for i in range(5):
        obtained_str, img = get_pic()
        print("got str: [" +  obtained_str + "], trash: [Trash]")
        if obtained_str == name:
            return True, img
        sleep(0.4)
    return False, img

print(verify_classes('Plastic', True))
