# Generated by Django 2.0.4 on 2018-04-13 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0004_sensor_coordinates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='longitude',
        ),
    ]