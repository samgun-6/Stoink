from __future__ import unicode_literals
import pandas as pd
from django.db import models
from tensorflow.keras.models import Sequential, load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.constraints import maxnorm
from sklearn import preprocessing
import numpy as np
import json as json
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential

class Stock(models.Model):

    name = models.CharField(max_length=30)
    txt = models.TextField(default="-")

    def __str__(self):
        return self.name

class Prediction:
    price: float

    def __init__(self, price):
        self.price = price


def train_model(csvfile):
    file_to_read = "data/" + str(csvfile)
    df = pd.read_csv(file_to_read, sep=',')

    # Initiating a Sequential model with keras
    model = tf.keras.models.Sequential()

    # Adding layers to the model
    model.add(tf.keras.layers.Dense(units=10, input_dim=5))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(100, activation='relu'))
    model.add(tf.keras.layers.Dense(51, activation='relu'))
    model.add(tf.keras.layers.Dense(units=1, activation='linear'))

    # Compiling the model
    opt = tf.keras.optimizers.Adam(lr=0.005)
    model.compile(loss='mean_squared_error', optimizer=opt, metrics=['accuracy'])

    # Declaring the label and features np.array
    column_features = []
    for col in df.columns:
        if col != "1m":
            column_features.append(col)

    # Slicing the dataset to features and labels
    y = df["1m"].to_numpy()
    X = df[column_features].to_numpy()

    # Normalizing
    X = preprocessing.normalize(X)

    # Splitting the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3727)

    # Fitting the model
    model.fit(X_train, y_train, epochs=100, batch_size=16)

    # IF no model in data base (this is a function in database.py)
    # THEN model_name = 'model_v1.h5'
    # ELSE load last model file and read name, then increase the version increment by 1 (model_v1 --> model_v2)
    # this gives us a new model in the database each time we run this function (train_model)

    # save model
    model_name = 'model_v1.h5'
    model.save(model_name)

def evaluate_model(model_name, X_test, y_test):
    model = load_model(model_name)
    # Model evaluation
    test_loss, test_acc = model.evaluate(X_test, y_test)
    return test_loss, test_acc

def make_prediction(model_name, data):
    model = load_model(model_name)
    # Code for prediction
    prediction = model.predict(data)
    return prediction

