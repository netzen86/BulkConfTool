from django.contrib import admin

from .models import SwitchPort, Vlans


class SwitchPortAdmin(admin.ModelAdmin):
    '''Админка портов коммутаторов.'''
    list_display = ('switch',
                    'port',
                    'socket',
                    'description')
    search_fields = ('socket', 'description')
    empty_value_display = '-пусто-'


class VlansAdmin(admin.ModelAdmin):
    '''Админка vlanov.'''
    list_display = ('switch',
                    'vid',
                    'vlan_name')
    search_fields = ('vid', 'vlan_name')
    empty_value_display = '-пусто-'


admin.site.register(SwitchPort, SwitchPortAdmin)
admin.site.register(Vlans, VlansAdmin)
