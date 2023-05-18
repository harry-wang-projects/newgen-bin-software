import cv2
import numpy as np
import os
import requests
import json

from time import sleep

from classification_specs import IMG_SIZE, number_of_colors 

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

camera = cv2.VideoCapture(0)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def send_image(tosend):
    print(type(tosend))
    url = 'https://recycling.student.isf.edu.hk/nggetcamera'
    myobj = {'picturearray', tosend}

    tosend = json.dumps(myobj, default = set_default)

    x = requests.post(url, json = tosend, verify = False)
    print("results")
    print(x.content)
    return 1

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

    new_array = np.asarray(new_array, dtype=np.float32).reshape(1, 224, 224, 3)

    new_array = (new_array / 127.5) - 1

    print(new_array)
    print(new_array.shape)

    camresult = send_image(new_array.tobytes())

    return camresult
    #print("Class:", class_name[2:], end="")
    #print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

        #lenofit = len(class_name)

        #return class_name[2:lenofit - 1]

get_pic()

def verify_classes(name):
    for i in range(10):
        obtained_str = get_pic()
        print("got str: [" +  obtained_str + "], trash: [Trash]")
        if obtained_str == name:
            return True
        sleep(0.2)
    return False

print(verify_classes('Trash'))
