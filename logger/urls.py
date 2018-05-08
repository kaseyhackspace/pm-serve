from django.urls import path, include
from .views import SensorList
from . import views

urlpatterns = [
    path('', SensorList.as_view(), name='index'),
    path('sensors/data/add', views.add_data, name='add_data'),
    path('sensors/map', views.map_sensors, name='map_sensor'),
    path('sensors/heatmap', views.heatmap, name='heatmap'),
    path('sensors/detail/<int:sensor_id>', views.sensor_detail, name='detail_sensor'),
    path('sensors/export/<int:sensor_id>', views.sensor_export, name='export_sensor'),
    path('sensors/export/', views.sensor_export_poly, name='export_poly'),
    path('sensors/crud/',  include('crudbuilder.urls')),
]
