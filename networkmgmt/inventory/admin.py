from django.contrib import admin


class DevicesAdmin(admin.ModelAdmin):
    """Админка устройств."""
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
