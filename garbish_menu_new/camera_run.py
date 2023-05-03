import cv2
import numpy as np
import os
from time import sleep
from keras.models import load_model

from classification_specs import IMG_SIZE, number_of_colors 
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("./converted_keras/keras_Model.h5", compile=False)

# Load the labels
class_names = open("./converted_keras/labels.txt", "r").readlines()

camera = cv2.VideoCapture(0)

def get_pic():

#    if number_of_colors == 1:
#        img_array = cv2.imread(1, cv2.IMREAD_GRAYSCALE)  # read in the image, convert to grayscale
#    else:
#        img_array = cv2.imread(1)
    camera = cv2.VideoCapture(0)
    return_value, img_array = camera.read()
    del(camera)

    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE), interpolation = cv2.INTER_AREA)

    new_array = np.asarray(new_array, dtype=np.float32).reshape(1, 224, 224, 3)

    new_array = (new_array / 127.5) - 1

    prediction = model.predict(new_array)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    lenofit = len(class_name)

    return class_name[2:lenofit - 1]

def verify_classes(name):
    for i in range(10):
        obtained_str = get_pic()
        print("got str: [" +  obtained_str + "], trash: [Trash]")
        if obtained_str == name:
            return True
        sleep(0.2)
    return False

print(verify_classes('Trash'))
