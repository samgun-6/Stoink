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
        new_urls = [path("upload-csv/", self.upload_csv)]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            print("action is post")
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


admin.site.register(AiModel, AiModelAdmin)
admin.site.register(CsvImportForm)
