import io
import os
import cv2
import numpy as np
import tensorflow as tf
import keras
import sklearn
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.constraints import UnitNorm
from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras import regularizers
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

import itertools  
import operator
import random
import time

import matplotlib.pyplot as plt

import pickle

import classification_specs

CATEGORIES = ['metal', 'paper', 'plastic', 'trash']

#load the array
x = pickle.load(open("./x.pickle", "rb"))
y = pickle.load(open("./y.pickle", "rb"))

x = x / 255.0

x = np.array(x)

y = np.array(y)

label_count = len(np.unique(y))
print(label_count)

#for multiple categories
y = tf.keras.utils.to_categorical(y, num_classes=label_count)

for i in range(len(y)):
    y[i] = y[i] * 1.0

#split data
xtrain, xval, ytrain, yval = train_test_split(x, y, train_size=0.9, test_size=0.1, random_state=42)
xtrain, xtest, ytrain, ytest = train_test_split(xtrain, ytrain, train_size=0.78, random_state=42)



print(type(x))
print(type(y))

print(y.shape)

#name of model

NAME = "garbage_recyclable_classification_model"

#maxpooling variables
dense_layer = 2
layer_size = 64
conv_layer = 2

#tensorboard stuff
tensorboard = TensorBoard(log_dir = './{}'.format(NAME))

tensorboard_callback = keras.callbacks.TensorBoard(log_dir = "./{}".format(NAME), histogram_freq = 1)
file_writer_cm = tf.summary.create_file_writer("./{}".format(NAME) + '/cm')


#functions
def plot_confusion_matrix(cm, class_names):
    """
    Returns a matplotlib figure containing the plotted confusion matrix.

    Args:
       cm (array, shape = [n, n]): a confusion matrix of integer classes
       class_names (array, shape = [n]): String names of the integer classes
    """

    figure = plt.figure(figsize=(8, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion matrix")
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)

    # Normalize the confusion matrix.
    cm = np.around(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], decimals=2)

    # Use white text if squares are dark; otherwise black.
    threshold = cm.max() / 2.

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        color = "white" if cm[i, j] > threshold else "black"
        plt.text(j, i, cm[i, j], horizontalalignment="center", color=color)

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return figure

def log_confusion_matrix(epoch, logs):

    # Use the model to predict the values from the test_images.
    test_pred_raw = model.predict(xtest)

    ytest_arg = np.argmax(ytest,axis=1)
    test_pred = np.argmax(model.predict(xtest),axis=1)
    print('Confusion Matrix')
    
#    test_pred = np.argmax(test_pred_raw, axis=1)

    # Calculate the confusion matrix using sklearn.metrics
    cm = sklearn.metrics.confusion_matrix(ytest_arg, test_pred)

    figure = plot_confusion_matrix(cm, class_names=CATEGORIES)
    cm_image = plot_to_image(figure)

    # Log the confusion matrix as an image summary.
    with file_writer_cm.as_default():
        tf.summary.image("Confusion Matrix", cm_image, step=epoch)

def plot_to_image(fig):
 # Saving the plot to a PNG in memory.
    bfr = io.BytesIO()
    plt.savefig(bfr, format='png')
    plt.close(fig)
    bfr.seek(0)
    # Converting PNG buffer to TF image
    image = tf.image.decode_png(bfr.getvalue(), channels=4)
    # Adding the batch dimension
    image = tf.expand_dims(image, 0)
    return image

#callbacks

cm_callback = keras.callbacks.LambdaCallback(on_epoch_end=log_confusion_matrix)




#initialize model
model = Sequential()

NAME = "{}-conv-{}-nodes{}-dense{}".format(conv_layer, layer_size, dense_layer, int(time.time()))
print(NAME)

#initial convolution
model.add(Conv2D(64, (3, 3), input_shape = x.shape[1:], activation = "relu", kernel_regularizer=regularizers.l2(l=0.01)))
model.add(Conv2D(64, (3, 3), activation = "relu", kernel_regularizer=regularizers.l2(l=0.01)))
model.add(Conv2D(128, (3, 3), activation = "relu", kernel_regularizer=regularizers.l2(l=0.01)))
model.add(MaxPooling2D(pool_size = (2, 2)))

#64 part
#model.add(Conv2D(64, (3, 3), activation = "relu"))
#model.add(MaxPooling2D(pool_size = (2, 2)))
#model.add(Dropout(0.4))

#128 part
model.add(Conv2D(128, (3, 3), activation = "relu", kernel_regularizer=regularizers.l2(l=0.01)))
model.add(Conv2D(256, (3, 3), activation = "relu", kernel_regularizer=regularizers.l2(l=0.01)))
model.add(MaxPooling2D(pool_size = (2, 2)))

#256 part
#model.add(Conv2D(256, (3, 3), activation = "relu", kernel_regularizer=regularizers.l2(l=0.01)))
#model.add(MaxPooling2D(pool_size = (2, 2)))
#model.add(Dropout(0.4))

#512 part
#model.add(Conv2D(512, (3, 3), activation = "relu", kernel_regularizer=regularizers.l2(l=0.01)))
#model.add(MaxPooling2D(pool_size = (2, 2)))
#model.add(Dropout(0.4))

#1024!
#model.add(Conv2D(1024, (3, 3), activation = "relu"))
#model.add(MaxPooling2D(pool_size = (2, 2)))


model.add(Flatten())

#end
#model.add(Dense(1024, activation = 'relu'))
model.add(Dense(180, activation = 'relu'))
model.add(Dropout(0.4))
model.add(Dense(90, activation = 'relu'))
model.add(Dropout(0.3))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.3))
model.add(Dense(label_count, activation = 'softmax'))


#compile and summarize model
model.compile(loss = "categorical_crossentropy", optimizer = "adam", metrics = ['accuracy'])

model.summary()

#run the model
model.fit(xtrain, ytrain, batch_size = 64, epochs = 30, callbacks = [tensorboard_callback, cm_callback], validation_data=(xval, yval))

model.save("current_testing_model.model")

