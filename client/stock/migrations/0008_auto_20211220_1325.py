# Generated by Django 3.2.9 on 2021-12-20 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_auto_20211220_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodel',
            name='dropout',
            field=models.FloatField(default=0.2),
        ),
        migrations.AddField(
            model_name='aimodel',
            name='inputlayer',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='aimodel',
            name='learningrate',
            field=models.FloatField(default=0.005),
        ),
        migrations.AddField(
            model_name='aimodel',
            name='secondlayer',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='aimodel',
            name='thirdlayer',
            field=models.IntegerField(default=51),
        ),
    ]