from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()
    address = models.CharField(max_length=255)
    organization = models.CharField(max_length=100)
    country = CountryField()

class Sensor(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    coordinates = models.PointField(null=True, blank=True,)
    def __str__(self):
        return self.name

class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    particulate_matter = models.FloatField()
    received_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField()

class Download(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sensors = models.ManyToManyField(Sensor)
    start_date = models.DateField()
    end_date = models.DateField()
