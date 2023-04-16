import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
from sklearn.metrics import confusion_matrix

import random
import time

import matplotlib.pyplot as plt

import pickle

#load the array
x = pickle.load(open("./x.pickle", "rb"))
y = pickle.load(open("./y.pickle", "rb"))

x = np.array(x)

y = np.array(y)


x = x / 255.0

print(type(x))
print(type(y))

print(x[1])
print(y[1])
print(x[2])
print(y[2])
print(x[3])
print(y[3])

#name of model

NAME = "garbage_recyclable_classification_model"
tensorboard = TensorBoard(log_dir="./{}".format(NAME))

#maxpooling variables
dense_layers = [0, 1, 2]
layer_sizes = [32, 64, 128]
conv_layers = [1, 2, 3]

for dense_layer in dense_layers:
	for layer_size in layer_sizes:
		for conv_layer in conv_layers:
			NAME = "{}-conv-{}-nodes{}-dense{}".format(conv_layer, layer_size, dense_layer, int(time.time()))
			print(NAME)
			model = Sequential()

			model.add(Conv2D(layer_size, (3, 3), input_shape = x.shape[1:]))
			model.add(Activation("relu"))
			model.add(MaxPooling2D(pool_size = (2, 2)))

			for i in range (conv_layer - 1):
				model.add(Conv2D(layer_size, (3, 3)))
				model.add(Activation("relu"))
				model.add(MaxPooling2D(pool_size = (2, 2)))

			model.add(Flatten())
			for i in range (dense_layer):
				model.add(Dense(layer_size))
				model.add(Activation("relu"))	

			model.add(Dense(1))
			model.add(Activation('sigmoid'))

			tensorboard = TensorBoard(log_dir = './{}'.format(NAME))

			model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ['accuracy'])
			model.fit(x, y, batch_size = 128, epochs = 1, validation_split = 0.2, callbacks = [tensorboard])


#model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ['accuracy'])

#model.fit(x, y, batch_size = 32, epochs = 3, validation_split = 0.3, callbacks = [tensorboard])

model.save("bad_testing_model.model")

#Predict
y_prediction = model.predict(x)

#Create confusion matrix and normalizes it over predicted (columns)
#result = confusion_matrix(y_test, y_prediction , normalize='pred')


