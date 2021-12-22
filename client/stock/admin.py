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
            model_file = request.FILES["csv_upload"]
            file_data = model_file.read().decode("utf-8")
            tempModel = models.DataSet()
            tempModel.title = model_file
            tempModel.data = file_data
            tempModel.save()
            print(tempModel.title)
            print(tempModel.data)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/dataset_upload.html", data)


class AiModelAdmin(admin.ModelAdmin):
    list_display = ("title", "version", "created", "loss", "accuracy", "learningrate", "inputlayer", "dropout", "secondlayer", "thirdlayer", "epochs", "batchsize", "split")

    def train_model(self, request):
        return render(request, "admin/model_upload.html", data)


admin.site.register(AiModel, AiModelAdmin)
admin.site.register(DataSet, DataSetAdmin)
