# Generated by Django 3.2.9 on 2021-12-20 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0011_datasetmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DataSetModel',
            new_name='DataSet',
        ),
    ]
