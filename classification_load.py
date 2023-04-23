import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

import random

import pickle

DATADIR = "D:/bin_data/more_training_pics"
#DATADIR = "/Users/harrywang/Downloads/kaggle_data/Garbage_classification/Folder"
CATEGORIES = ['metal', 'paper', 'plastic', 'trash']

IMG_SIZE = 128

training_data = []

def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)
        print(class_num)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img))
                print(type(img_array))
                if img_array.shape[0] > img_array.shape[1]:
                    print(img_array.shape)
                    img_array = cv2.rotate(img_array, cv2.ROTATE_90_CLOCKWISE)

                gauss_noise = np.zeros((img_array.shape[0], img_array.shape[1], 3), dtype = np.uint8)
                cv2.randn(gauss_noise, 128, 20)
                gauss_noise = (gauss_noise * 0.1).astype(np.uint8)
                img_array = cv2.add(img_array, gauss_noise)

                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
                #plt.imshow(new_array)
                #plt.show()
            except Exception as e:
                print(e)
                pass
            

create_training_data()
print(len(training_data))

random.shuffle(training_data)
print(training_data[1])

x = []
y = []
i = 0

for features, label in training_data:
    x.append(features)
    y.append(label)
    i+=1

print('length: ', i)
print('Image Dimensions :', x[1].shape)
print('label Dimensions :', type(y))

x = np.array(x).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
y = np.array(y).reshape(-1, 1)

pickle_out = open("./x.pickle", "wb")
pickle.dump(x, pickle_out)
pickle_out.close()

pickle_out = open("./y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()

#pickle_in = open("./x.pickle", "rb")
#x = pickle.load(pickle_in)
#print(x[1])


