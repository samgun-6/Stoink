from __future__ import unicode_literals

import pandas as pd
from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import forms
from django.shortcuts import render, get_object_or_404
from django.urls import path
import pandas as pd
from django.db import models
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import tensorflow as tf

from . import models
from .models import AiModel, DataSet
#from .admin import AiModelAdmin, DataSetAdmin

admin.site.site_header = "Admin page for managing training, loading, evaluating models etc."
admin.site.unregister(Group)


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


class DataSetAdmin(admin.ModelAdmin):
    list_display = ("title", "created",)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path("upload-dataset/", self.upload_dataset)]
        return new_urls + urls

    def upload_dataset(self, request):
        if request.method == "POST":
            # requesting the data
            model_file = request.FILES["csv_upload"]
            # decoding to String
            file_data = model_file.read().decode("utf-8")
            # declaring model with attributes and saving it
            tempModel = models.DataSet()
            tempModel.title = model_file

            #Splitting the filedata to get column names
            column = file_data.split("\r\n", 1)
            column = str(column[0])
            column = column.split(",", 8)

            # converting the string into a dataframe to be able to save as json object (attribute of DataSet model)
            data = file_data
            df = pd.DataFrame(data=[x.split(',') for x in data.split('\r\n')])
            #deleting first row, for some realson after above function, it adds the column names as first data row....
            print(df.tail(1))
            print(df.head(1))
            df = df.iloc[1:-1, :]
            print(df.head(1))
            print(df.tail(1))
            # Assiging the right column names
            df.columns = column

            tempModel.putframe(df)
            tempModel.save()
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/dataset_upload.html", data)


class AiModelAdmin(admin.ModelAdmin):
    list_display = ("title", "train_button", "train","version", "deployed", "dataset", "created", "loss", "accuracy", "learningrate", "inputlayer", "dropout", "secondlayer", "thirdlayer", "epochs", "batchsize", "split")


    def get_urls(self):
        print("IM IN THE RIGHT FUNCTION")
        urls = super().get_urls()
        my_urls = [
            path('train/<int:title>/', view =self.train_model, name="train"),
        ]
        return my_urls + urls

    def train_model(self, request, title):
        print("Called the train functuon")
        print("HERE I AM")
        target = get_object_or_404(AiModel, pk=title)
        print(target)
        df = pd.read_csv("data/topFiveFeats.csv", sep=',')
        # CLEAN DATAset!!!!!!!!!!

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

        return render(request, "admin/base.html")


    #def my_button(self, obj):
    #    return mark_safe('<form action = "setModel" method = "POST">'
    #            '<button type = "submit" name = "pk" value = "title" id = "pk"> Deploy </button>'
    #            '</form>')




admin.site.register(AiModel, AiModelAdmin)
admin.site.register(DataSet, DataSetAdmin)
