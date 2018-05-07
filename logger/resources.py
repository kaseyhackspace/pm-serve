from import_export import resources
from .models import SensorData

class SensorDataResource(resources.ModelResource):
    class Meta:
        model = SensorData

class MulSensorDataResource(resources.ModelResource):
    class Meta:
        model = SensorData
