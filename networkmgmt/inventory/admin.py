from django.contrib import admin

from .models import Devices, Configurations


class DevicesAdmin(admin.ModelAdmin):
    '''Админка устройств.'''
    list_display = ('device_type',
                    'ip_add',
                    'author',
                    'serial_num',
                    'model',
                    'hostname',
                    'os_version',
                    'vendor')
    search_fields = ('serial', 'ip')
    empty_value_display = '-пусто-'


class ConfigurationsAdmin(admin.ModelAdmin):
    '''Админка конфигураций'''
    list_display = ('device', 'configuration')
    search_fields = ('device',)
    empty_value_display = '-пусто-'


admin.site.register(Devices, DevicesAdmin)
admin.site.register(Configurations, ConfigurationsAdmin)
