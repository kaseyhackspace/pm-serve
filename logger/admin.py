from django.contrib.gis import admin
from .models import *

admin.site.register(Profile, admin.OSMGeoAdmin)
admin.site.register(Sensor, admin.OSMGeoAdmin)
admin.site.register(SensorData, admin.OSMGeoAdmin)
admin.site.register(Download, admin.OSMGeoAdmin)
# Register your models here.
