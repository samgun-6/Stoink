from __future__ import unicode_literals
from django.db import models
import pandas as pd
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



# Loading the data from CSV into panadas dataframe
df = pd.read_csv (r'..\data\topFiveFeats211207.csv', sep=',')

# Initiating a Sequential model with keras
model = tf.keras.models.Sequential()

# Adding layers to the model
model.add(tf.keras.layers.Dense(units = 10, input_dim=5))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(51, activation='relu'))
model.add(tf.keras.layers.Dense(units = 1, activation = 'linear'))

# Compiling the model
opt = tf.keras.optimizers.Adam(lr=0.005)
model.compile(loss = 'mean_squared_error', optimizer = opt, metrics=['accuracy'])

# Declaring the label and features np.array
column_features = ["reportedEPS","totalNonCurrentAssets","totalCurrentAssets","otherNonCurrentLiabilities", "cashflowFromFinancing"]

# Slicing the dataset to features and labels
y = df["1m"].to_numpy()
X = df[column_features].to_numpy()

# Normalizing
X = preprocessing.normalize(X)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3727)

# Fitting the model
model.fit(X_train, y_train, epochs = 100, batch_size = 16)

# Code for evaluating
# Model evaluation
#test_loss, test_acc = model.evaluate(X_test, y_test)
# Printing
#print('\nTest accuracy:', test_acc)

# Code for prediction
# prediction
#predictions = model.predict(X_test)
#print(predictions)