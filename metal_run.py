import cv2
import os
import tensorflow as tf

DATADIR = "D:/bin_data/testing_pictures"
CATEGORIES = ['metal', 'non-metal']


def prepare(file_path):
    IMG_SIZE = 128  # 50 in txt-based
    img_array = cv2.imread(file_path)  # read in the image, convert to grayscale
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)  # return the image with shaping that TF wants.

model = tf.keras.models.load_model("./metal_testing_model.model")

def predict(filepath):
    print(filepath)
    prediction = model.predict([prepare(filepath)])
    prediction[0][0] = round(prediction[0][0] * 100)    
    prediction[0][1] = round(prediction[0][1] * 100)

    print(prediction)

    if prediction[0][0] > prediction[0][1]:
        print(CATEGORIES[0])
    else:
        print(CATEGORIES[1])

for filename in os.listdir(DATADIR):
    with open(os.path.join(DATADIR, filename), 'r') as f: 
        pathstr = f.name
        predict(pathstr)
