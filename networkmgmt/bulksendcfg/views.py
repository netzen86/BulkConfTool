from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.send_cmd import run_parallel_session
from inventory.models import Devices
from .forms import CommandsForm
from django.forms.models import model_to_dict
import json


@login_required
def bulk_send_cmd(request):
    # if this is a POST request we need to process the form data
    template = 'bulksendcfg/bulkcfg.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommandsForm(request.POST)
        devices = []
        for obj in Devices.objects.all():
            devices.append({
                'device_type': model_to_dict(obj)['device_type'],
                'ip': model_to_dict(obj)['ip_add'],
                'username': request.user.username,
                'password': request.user.dev_password,
                })
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            run_parallel_session(
                devices,
                'output_cmd.txt',
                json.loads(form.cleaned_data['commands']),
                request
                )
            # redirect to a new URL:
            return render(request, template, {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommandsForm()

    return render(request, template, {'form': form})
