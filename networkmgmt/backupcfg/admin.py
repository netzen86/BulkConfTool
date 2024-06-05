from django.contrib import admin


from .models import StartTime, Days


class DaysAdmin(admin.ModelAdmin):
    '''День запуска резервного копирования'''
    search_fields = ('days',)
    empty_value_display = '-пусто-'


class StartTimeAdmin(admin.ModelAdmin):
    '''Время запуска резервного копирования.'''
    list_display = ('time',)
    search_fields = ('days', 'time')
    empty_value_display = '-пусто-'


admin.site.register(StartTime, StartTimeAdmin)
admin.site.register(Days, DaysAdmin)
