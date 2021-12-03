from __future__ import unicode_literals
from django.db import models
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM

class Stock(models.Model):

    name = models.CharField(max_length=30)
    txt = models.TextField(default="-")

    def __str__(self):
        return self.name

class Prediction:
    date: str
    price: float

    def __init__(self, date, price):
        self.date = date
        self.price = price


# Here is the model, the first time when it runs, it will generate a model file called lstm_1.h5
# if we have the h5 file, we can comment out the code

# Load Data
# add other 198 stock names later 
stocks = ['AAPL']

for stock_index in range(0, len(stocks)):
    stock = stocks[stock_index]
    # read data
    data = pd.read_csv("data/monthly-data.csv")
    # get time from timestamp
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    # calculate time duration
    start = data.TIME.min()
    end = data.TIME.max()
    mask = (data['timestamp'] > start) & (data['timestamp'] <= end)
    # extract all data in the time duration
    data = data.loc[mask]

    # Precess data
    # use MinMaxScaler to transform each feature a giving range 0-1
    scaler = MinMaxScaler(feature_range=(0,1))

    scaled_data = scaler.fit_transform(data['CLOSE'].values.reshape(-1,1))


    # How many days back should the prediction be based on
    prediction_days = 365

    x_train = []
    y_train = []

    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x - prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Build LSTM model
    model = Sequential()

    model.add(LSTM(units=5, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=5, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=5))
    model.add(Dropout(0.2))
    model.add(Dense(units=5))  # Prediction of the next closing value

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=1, batch_size=32)

    model_fname = 'lstm_1.h5'
    model.save(model_fname)
    # check model architecture
    n_model = load_model(model_fname)
    n_model.summary()
