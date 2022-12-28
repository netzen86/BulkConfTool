from django.contrib import admin


class DevicesAdmin(admin.ModelAdmin):
    """Админка устройств."""
    list_display = ('*')
    search_fields = ('lastname', 'username')
    empty_value_display = '-пусто-'
