from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import ListView
from .models import *
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

from .forms import SensorExportForm
from .forms import MulSensorExportForm
from .resources import SensorDataResource
from .resources import MulSensorDataResource

from django.contrib.auth.decorators import login_required

class SensorList(ListView):
    model = Sensor

@login_required
def sensor_export_poly(request):

    if request.method == 'POST':
        form = MulSensorExportForm(request.POST)

        if form.is_valid():
            sensor_data_resource = MulSensorDataResource()
            sensors = Sensor.objects.filter(pk__in=json.loads(form.cleaned_data['mul_sensors']))
            queryset = SensorData.objects.filter(sensor__in=sensors).filter(created_at__gte = form.cleaned_data['start_date']).filter(created_at__lte = form.cleaned_data['end_date'])
            dataset = sensor_data_resource.export(queryset)

            download = Download()
            download.owner = request.user
            download.sensors_set = sensors
            download.start_date = form.cleaned_data['start_date']
            download.end_date = form.cleaned_data['end_date']
            download.save()

            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="sensors.csv"'
            return response
    else:
        sensors = Sensor.objects.all()
        form = SensorExportForm()
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        return render(request, 'logger/export-poly.html', {'form': form, 'sensors': sensors,'date': date})

@login_required
def sensor_export(request,sensor_id):

    if request.method == 'POST':
        form = SensorExportForm(request.POST)

        if form.is_valid():
            sensor_data_resource = SensorDataResource()
            sensor = Sensor.objects.get(id=sensor_id)
            queryset = SensorData.objects.filter(sensor=sensor).filter(created_at__gte = form.cleaned_data['start_date']).filter(created_at__lte = form.cleaned_data['end_date'])
            print(queryset)
            dataset = sensor_data_resource.export(queryset)

            download = Download()
            download.owner = request.user
            download.sensors_set = [sensor]
            download.start_date = form.cleaned_data['start_date']
            download.end_date = form.cleaned_data['end_date']
            download.save()

            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="sensor.csv"'
            return response


    # if a GET (or any other method) we'll create a blank form
    else:
        sensor = Sensor.objects.get(id=sensor_id)
        form = SensorExportForm()
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        return render(request, 'logger/export-form.html', {'form': form, 'sensor': sensor,'date': date})


@csrf_exempt
def add_data(request):
    if request.method == 'POST':
        data = request.POST
        sensor = Sensor.objects.get(id=data['node_id'])
        sensor_data = SensorData()
        sensor_data.sensor = sensor
        sensor_data.particulate_matter = data['density']
        sensor_data.created_at = datetime.datetime.fromtimestamp(
        int(data['timestamp']))
        sensor_data.save()
    return JsonResponse(data)

def map_sensors(request):
    sensors = Sensor.objects.all()
    for sensor in sensors:
        if sensor.sensordata_set.last():
            sensor.pm = sensor.sensordata_set.order_by('created_at').last().particulate_matter
        else:
            sensor.pm = 0
    return render(request,'logger/map_sensors.html',{'sensors': sensors})

def heatmap(request):
    sensors = Sensor.objects.all()
    data = []
    for sensor in sensors:
        if sensor.sensordata_set.last():
            pm = sensor.sensordata_set.order_by('created_at').last().particulate_matter
        else:
            pm = 0
        data.append([sensor,pm])
    return render(request,'logger/heatmap.html',{'data': data})

def sensor_detail(request,sensor_id):
    sensor = Sensor.objects.get(id=sensor_id)
    data = sensor.sensordata_set.order_by('-created_at').all()
    for log in data:
        log.created_at = log.created_at - datetime.timedelta(hours = 8)
    return render(request,'logger/sensor_detail.html',{'sensor': sensor, 'data':data})
