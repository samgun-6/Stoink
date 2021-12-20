from __future__ import unicode_literals
import pandas as pd
from django.db import models
from tensorflow.keras.models import Sequential, load_model
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import tensorflow as tf


class AiModel(models.Model):
    # Title is also the name of the file that holds the model, which we load from the repo as a .h5 file
    title = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    loss = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)
    learningrate = models.FloatField(default=0.005)
    dropout = models.FloatField(default=0.2)
    inputlayer = models.IntegerField(default=10)
    secondlayer = models.IntegerField(default=100)
    thirdlayer = models.IntegerField(default=51)
    epochs = models.IntegerField(default=100)
    batchsize = models.IntegerField(default=16)
    split = models.FloatField(default=0.3727)

    def __str__(self):
        return self.title

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def train_model(self, file_name):
        file_to_read = "data/" + str(file_name)
        df = pd.read_csv(file_to_read, sep=',')

        # Randomly shuffles the rows, better for training the model later
        # Also resetting the Index for the dataframe
        df = df.sample(frac=1).reset_index(drop=True)

        # Initiating a Sequential model with keras
        model = tf.keras.models.Sequential()

        # Adding layers to the model
        model.add(tf.keras.layers.Dense(units=self.inputlayer, input_dim=5))
        model.add(tf.keras.layers.Dropout(self.dropout))
        model.add(tf.keras.layers.Dense(self.secondlayer, activation='relu'))
        model.add(tf.keras.layers.Dense(self.thirdlayerlayer, activation='relu'))
        model.add(tf.keras.layers.Dense(units=1, activation='linear'))

        # Compiling the model
        opt = tf.keras.optimizers.Adam(lr=self.learningrate)
        model.compile(loss='mean_squared_error', optimizer=opt, metrics=['accuracy'])

        # Declaring the label and features np.array
        column_features = []
        for col in df.columns:
            if col != "1m":
                if col != "symbol":
                    if col != "timestamp":
                        column_features.append(col)

        # Slicing the dataset to features and labels
        y = df["1m"].to_numpy()
        X = df[column_features].to_numpy()

        # Normalizing
        X = preprocessing.normalize(X)

        # Splitting the dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.split)

        # Fitting the model
        model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batchsize)

        # IF no model in data base (this is a function in database.py)
        # THEN model_name = 'model_v1.h5'
        # ELSE load last model file and read name, then increase the version increment by 1 (model_v1 --> model_v2)
        # this gives us a new model in the database each time we run this function (train_model)

        # save model
        model_name = str(self.title)
        model.save(model_name)

    def evaluate_model(self, X_test, y_test):
        model = load_model(self.title)
        # Model evaluation
        test_loss, test_acc = model.evaluate(X_test, y_test)
        self.loss = test_loss
        self.accuracy = test_acc
        return test_loss, test_acc

    def make_prediction(self, data):
        model = load_model(self.title)
        # Code for prediction
        prediction = model.predict(data)
        return prediction



class Prediction:
    price: float

    def __init__(self, price):
        self.price = price


