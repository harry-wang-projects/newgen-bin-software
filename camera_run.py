import cv2
import numpy as np
import os
import tensorflow as tf

from classification_specs import IMG_SIZE, number_of_colors 

CATEGORIES = ['metal', 'paper', 'plastic', 'trash']

model = tf.keras.models.load_model("./tiny_good_model1.model")

def get_pic():

#    if number_of_colors == 1:
#        img_array = cv2.imread(1, cv2.IMREAD_GRAYSCALE)  # read in the image, convert to grayscale
#    else:
#        img_array = cv2.imread(1)
    camera = cv2.VideoCapture(0)
    return_value, img_array = camera.read()
    del(camera)

    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing

    new_array = new_array / 255.0

    new_array = np.array(new_array).reshape(-1, IMG_SIZE, IMG_SIZE, number_of_colors)  # return the image with shaping that TF wants.

    prediction = model.predict(new_array)
    for i in range(4):
        prediction[0][i] = round(prediction[0][i] * 100)    

    max_category = -1
    print(prediction)
    for i in range(4):
        if(round(prediction[0][i] / 100) == 1):
            max_category = i


    return CATEGORIES[max_category]
