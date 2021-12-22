from __future__ import unicode_literals
import pandas as pd
from django.contrib.postgres.fields import JSONField
from django.db import models
from tensorflow.keras.models import Sequential, load_model
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import tensorflow as tf


class DataSet(models.Model):
    title = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    data = JSONField(default='This is empty')

    def putframe(self, cls, dataframe):
        storeddataframe = cls(data=dataframe.to_json(orient='split'))
        storeddataframe.save()
        return storeddataframe

    def loadframe(self):
        return pd.read_json(self.data, orient='split')

    def __str__(self):
        return self.title

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title


#class Row(models.Model):
#    label = models.FloatField(default=0.0)
#    reportedEPS = models.FloatField(default=0.0)
#    totalNonCurrentAssets = models.FloatField(default=0.0)
#    depreciation = models.FloatField(default=0.0)
#    proceedsFromRepaymentsOfShortTermDebt = models.FloatField(default=0.0)
#    currentAccountsPayable = models.FloatField(default=0.0)
#    symbol = models.CharField(max_length=30)
#    timestamp = models.CharField(max_length=30)
#    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)

 #   def get_data_prediction(self):
#        list_of_data = [self.label, self.reportedEPS, self.totalNonCurrentAssets, self.depreciation, self.proceedsFromRepaymentsOfShortTermDebt
#                        , self.currentAccountsPayable]
#        return list_of_data

#    def get_all_data(self):
#        list_of_data = [str(self.label), str(self.reportedEPS), str(self.totalNonCurrentAssets), str(self.depreciation),
#                        str(self.proceedsFromRepaymentsOfShortTermDebt)
#            , str(self.currentAccountsPayable), str(self.symbol), str(self.timestamp)]
#        return list_of_data

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
    version = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_titleversion(self):
        temp = self.title + str(self.version)
        return temp

    def set_title(self, title):
        self.title = title

    def train_model(self, file_name):
        file_to_read = "data/" + str(file_name)
        df = pd.read_csv(file_to_read, sep=',')
        #CLEAN DATAset!!!!!!!!!!

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

        # Updating the version of the model
        self.version = self.version + 1

        # save model
        # Maybe we need to add .h5 to be able to save it?
        print(self.get_titleversion())
        model.save(self.get_titleversion())

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


