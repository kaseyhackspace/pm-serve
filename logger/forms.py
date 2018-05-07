from django import forms
import datetime

class SensorExportForm(forms.Form):
    sensor = forms.IntegerField(label='Sensor')
    start_date = forms.DateField(label='Start Date',initial=datetime.date.today)
    end_date = forms.DateField(label='End Date',initial=datetime.date.today)

class MulSensorExportForm(forms.Form):
    mul_sensors = forms.CharField(label='Sensors')
    start_date = forms.DateField(label='Start Date',initial=datetime.date.today)
    end_date = forms.DateField(label='End Date',initial=datetime.date.today)
