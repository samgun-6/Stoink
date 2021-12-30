from __future__ import unicode_literals

import pandas as pd
from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import forms
from django.shortcuts import render
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
    list_display = ("title", "train_button","version", "deployed", "dataset", "created", "loss", "accuracy", "learningrate", "inputlayer", "dropout", "secondlayer", "thirdlayer", "epochs", "batchsize", "split")

    def get_urls(self):
        print("IM IN THE RIGHT FUNCTION")
        urls = super().get_urls()
        my_urls = [
            path('train-model/<int:pk>/', self.train_model, name="admin_train_model"),
        ]
        return my_urls + urls

    def train_model(self, request, pk):
        print("IM IN THE RIGHT FUNCTION")
        

        return render(request, "admin/base.html")


    #def my_button(self, obj):
    #    return mark_safe('<form action = "setModel" method = "POST">'
    #            '<button type = "submit" name = "pk" value = "title" id = "pk"> Deploy </button>'
    #            '</form>')




admin.site.register(AiModel, AiModelAdmin)
admin.site.register(DataSet, DataSetAdmin)
