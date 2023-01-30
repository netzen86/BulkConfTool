from django.urls import path
from .views import switch_port_mgmt

app_name = 'swportmgmt'


urlpatterns = [
    path('', switch_port_mgmt, name='switch_port_mgmt'),
]
