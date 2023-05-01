import cv2
import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt

from classification_specs import IMG_SIZE, number_of_colors 

DATADIR = "D:/bin_data/testing_pictures"
CATEGORIES = ['metal', 'paper', 'plastic', 'trash']


def prepare(file_path):
    if number_of_colors == 1:
        img_array = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)  # read in the image, convert to grayscale
    else:
        img_array = cv2.imread(file_path)

    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing

    gauss_noise = np.zeros((img_array.shape[0], img_array.shape[1], number_of_colors), dtype = np.uint8)
    cv2.randn(gauss_noise, IMG_SIZE, 20)

    gauss_noise = (gauss_noise * 0.2).astype(np.uint8)
    print(gauss_noise.shape)

    new_array = cv2.add(img_array, gauss_noise)


    new_array = cv2.resize(new_array, (IMG_SIZE, IMG_SIZE))

    new_array = new_array / 255.0
    
    #plt.imshow(new_array, cmap = 'gray')
    #plt.show()

    return np.array(new_array).reshape(-1, IMG_SIZE, IMG_SIZE, number_of_colors)  # return the image with shaping that TF wants.

model = tf.keras.models.load_model("./current_testing_model.model")

def predict(filepath):
    print(filepath)
    prediction = model.predict([prepare(filepath)])
    for i in range(4):
        prediction[0][i] = round(prediction[0][i] * 100)    

    print(prediction)
    for i in range(4):
        if(round(prediction[0][i] / 100) == 1):
            print(CATEGORIES[i])


for filename in os.listdir(DATADIR):
    with open(os.path.join(DATADIR, filename), 'r') as f: 
        pathstr = f.name
        predict(pathstr)
