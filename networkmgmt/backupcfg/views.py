from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from core.send_cmd import run_parallel_session
# from inventory.models import Devices
from .forms import BackUpForm
# from django.forms.models import model_to_dict
# from django.core.cache import cache
# import json


@login_required
def backup_cfg(request):
    # if this is a POST request we need to process the form data
    template = 'backupcfg/backupcfg.html'
    form = BackUpForm(request.POST)
    return render(request, template, {'form': form})
