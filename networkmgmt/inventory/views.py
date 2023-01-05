from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import Devices
from core.views import make_pntr


@login_required(login_url='auth/login')
def index(request):
    """Главная страница"""
    template = 'inventory/index.html'
    title = 'Настройка группы устройств'
    context = {
        'title': title
    }
    context.update(make_pntr(Devices.objects.all(), request))
    return render(request, template, context)
