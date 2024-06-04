from django.contrib import admin


from .models import StartTime


class StartTimeAdmin(admin.ModelAdmin):
    '''Время запуска резервного копирования.'''
    list_display = ('date',
                    'time',)
    search_fields = ('date', 'time')
    empty_value_display = '-пусто-'


admin.site.register(StartTime, StartTimeAdmin)
