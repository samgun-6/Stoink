# Generated by Django 3.0.3 on 2020-07-03 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_auto_20200513_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='divest',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='invest',
        ),
    ]
