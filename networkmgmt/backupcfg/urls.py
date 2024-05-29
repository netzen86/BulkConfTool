from django.urls import path
from .views import backup_cfg

app_name = 'backupcfg'


urlpatterns = [
    path('', backup_cfg, name='backup_cfg'),
]
