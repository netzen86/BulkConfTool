from django.urls import path
from .views import bulk_send_cmd

app_name = 'bulksendcfg'


urlpatterns = [
    path('', bulk_send_cmd, name='bulk_send_cmd'),
]
