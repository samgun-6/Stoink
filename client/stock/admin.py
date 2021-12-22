import pandas as pd
from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import forms
from django.shortcuts import render
from django.urls import path

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
            #print("-------- COLUMN _______")
            #print(column)
            #print(type(column))
            #testing to dataframe
            #print("-------- DATAFRAME _______")
            # converting the string into a dataframe to be able to save as json object (attribute of DataSet model)
            data = file_data
            df = pd.DataFrame(data=[x.split(',') for x in data.split('\r\n')])
            df = df.iloc[1:, :]
            # Assiging the right column names
            df.columns= column
            #print(df)

            tempModel.putframe(df)
            tempModel.save()
            #print(tempModel.title)
            #print(tempModel.data)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/dataset_upload.html", data)


class AiModelAdmin(admin.ModelAdmin):
    list_display = ("title", "version", "created", "loss", "accuracy", "learningrate", "inputlayer", "dropout", "secondlayer", "thirdlayer", "epochs", "batchsize", "split")

    def train_model(self, request):
        return render(request, "admin/model_upload.html", data)


admin.site.register(AiModel, AiModelAdmin)
admin.site.register(DataSet, DataSetAdmin)
