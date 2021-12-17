from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import forms
from django.shortcuts import render
from django.urls import path

from .models import AiModel

admin.site.site_header = "Admin page for managing training, loading, evaluating models etc."
admin.site.unregister(Group)


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


class AiModelAdmin(admin.ModelAdmin):
    list_display = ("title", "created")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path("upload-model/", self.upload_model)]
        return new_urls + urls


    def upload_model(self, request):

        if request.method == "POST":
            model_file = request.FILES["csv_upload"]
            file_data = model_file.read().decode("utf-8")
            print(file_data)
            model_data = file_data.split("/n")
            print("sucessfully imported the csv file")
            print(model_data)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/model_upload.html", data)


admin.site.register(AiModel, AiModelAdmin)
