import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import confusion_matrix

import random
import time

import matplotlib.pyplot as plt

import pickle

from confusion_matrix import plot_confusion_matrix


#load the array
x = pickle.load(open("./x.pickle", "rb"))
y = pickle.load(open("./y.pickle", "rb"))

x = np.array(x)

y = np.array(y)

label_count = len(np.unique(y))
print(label_count)

#for multiple categories
y = tf.keras.utils.to_categorical(y, num_classes=5)

#x = x / 255.0

print(type(x))
print(type(y))

print(y.shape)

#name of model

NAME = "garbage_recyclable_classification_model"
tensorboard = TensorBoard(log_dir="./{}".format(NAME))

#maxpooling variables
dense_layer = 2
layer_size = 64
conv_layer = 2


#initialize model

NAME = "{}-conv-{}-nodes{}-dense{}".format(conv_layer, layer_size, dense_layer, int(time.time()))
print(NAME)
model = Sequential()

#initial convolution
model.add(Conv2D(64, (7, 7), input_shape = x.shape[1:], activation = "relu"))
model.add(MaxPooling2D(pool_size = (2, 2)))


#64 part
#model.add(Conv2D(64, (3, 3), activation = "relu"))
#model.add(MaxPooling2D(pool_size = (2, 2)))


#128 part
model.add(Conv2D(128, (3, 3), activation = "relu"))
model.add(MaxPooling2D(pool_size = (2, 2)))


#256 part
model.add(Conv2D(256, (3, 3), activation = "relu"))
model.add(MaxPooling2D(pool_size = (2, 2)))

#512 part
model.add(Conv2D(512, (3, 3), activation = "relu"))
model.add(MaxPooling2D(pool_size = (2, 2)))

#1024!
#model.add(Conv2D(1024, (3, 3), activation = "relu"))
#model.add(MaxPooling2D(pool_size = (2, 2)))


model.add(Flatten())
model.add(Dropout(0.5))

#end
#model.add(Dense(1024, activation = 'relu'))
model.add(Dense(512, activation = 'relu'))
model.add(Dense(256, activation = 'relu'))
model.add(Dense(128, activation = 'relu'))
model.add(Dense(64, activation = 'relu'))
model.add(Dense(label_count, activation = 'softmax'))

#compile and summarize model
model.compile(loss = "categorical_crossentropy", optimizer = "adam", metrics = ['accuracy'])

model.summary()

#tensorboard stuff
tensorboard = TensorBoard(log_dir = './{}'.format(NAME))

tensorboard_callback = keras.callbacks.TensorBoard(log_dir = logdir, histogram_freq = 1)
file_writer_cm = tf.summary.create_file_writer(logdir + '/cm')

cm_callback = keras.callbacks.LambdaCallback(on_epoch_end=log_confusion_matrix)

model.fit(x, y, batch_size = 128, epochs = 20, validation_split = 0.3, callbacks = [tensorboard])


#model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ['accuracy'])

#model.fit(x, y, batch_size = 32, epochs = 3, validation_split = 0.3, callbacks = [tensorboard])

model.save("bad_testing_model.model")

#Predict
y_prediction = model.predict(x)


