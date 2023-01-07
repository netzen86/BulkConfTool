from django.urls import path
from . import views

app_name = 'core'


urlpatterns = [
    path('', views.index, name='index'),
    path('save_file/', views.save_file, name='save_file'),
]
