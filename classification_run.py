import cv2
import os
import tensorflow as tf

DATADIR = "/Users/harrywang/Desktop/testing_pictures"
CATEGORIES = ['glass', 'metal', 'paper', 'plastic', 'trash']


def prepare(file_path):
    IMG_SIZE = 128  # 50 in txt-based
    img_array = cv2.imread(file_path)  # read in the image, convert to grayscale
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)  # return the image with shaping that TF wants.

model = tf.keras.models.load_model("./bad_testing_model.model")

def predict(filepath):
    print(filepath)
    prediction = model.predict([prepare(filepath)])
    for i in range(5):
        prediction[0][i] = round(prediction[0][i] * 100)    

    print(prediction)
    for i in range(5):
        if(round(prediction[0][i] / 100) == 1):
            print(CATEGORIES[i])

for filename in os.listdir(DATADIR):
    with open(os.path.join(DATADIR, filename), 'r') as f: 
        pathstr = f.name
        predict(pathstr)
