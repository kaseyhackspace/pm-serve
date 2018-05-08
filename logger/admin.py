from django.contrib.gis import admin
from .models import *


class SensorAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'description', 'address','coordinates')
    list_filter = ('owner',)
    exclude = ['owner']

    def queryset(self, request):
        qs = super(EntryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(owner = request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if request.user.is_superuser or obj.owner == request.user:
            return True
        else:
            return False

    has_delete_permission = has_change_permission

admin.site.register(Profile, admin.OSMGeoAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(SensorData, admin.OSMGeoAdmin)
admin.site.register(Download, admin.OSMGeoAdmin)
# Register your models here.
