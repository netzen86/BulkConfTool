from django.urls import path
from . import views

app_name = 'bulksendcfg'


urlpatterns = [
    path('',
         views.index, name='index'),
]
