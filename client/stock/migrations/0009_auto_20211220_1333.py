# Generated by Django 3.2.9 on 2021-12-20 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0008_auto_20211220_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodel',
            name='batchsize',
            field=models.IntegerField(default=16),
        ),
        migrations.AddField(
            model_name='aimodel',
            name='epochs',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='aimodel',
            name='split',
            field=models.FloatField(default=0.3727),
        ),
    ]
