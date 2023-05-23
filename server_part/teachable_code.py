from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import os

from classification_specs import IMG_SIZE, number_of_colors

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("/home/0012113/newgen-bin-software/server_part/may22_multi_model/keras_model.h5", compile=False)

# Load the labels
class_names = open("/home/0012113/newgen-bin-software/server_part/may22_multi_model/labels.txt", "r").readlines()

DATADIR = "./testing_pictures"
CATEGORIES = ['metal', 'paper', 'plastic', 'trash']


def prepare(file_path):
#    if number_of_colors == 1:
#        img_array = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)  # read in the image, convert to grayscale
#    else:
    img_array = cv2.imread(file_path)

    img_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)

    img_array = np.asarray(img_array, dtype=np.float32).reshape(1, 224, 224, 3)

    img_array = (img_array / 127.5) - 1

    return img_array  # return the image with shaping that TF wants.

#model = tf.keras.models.load_model("./current_testing_model.model")

def predict(filepath):
    print(filepath)
    prediction = model.predict(prepare(filepath))

    print(prediction)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    return class_name[2:], str(np.round(confidence_score * 100))[:-2]

def predict_array(array):
    prediction = model.predict(array)

    print(prediction)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    return class_name[2:], str(np.round(confidence_score * 100))[:-2], prediction

for filename in os.listdir(DATADIR):
    with open(os.path.join(DATADIR, filename), 'r') as f:
        pathstr = f.name
        predict(pathstr)
