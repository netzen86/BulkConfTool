from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.send_cmd import run_parallel_session
from inventory.models import Devices
from .forms import CommandsForm
from django.forms.models import model_to_dict
from django.core.cache import cache
import json


@login_required
def bulk_send_cmd(request):
    # if this is a POST request we need to process the form data
    template = 'bulksendcfg/bulkcfg.html'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommandsForm(request.POST)
        devices = []
        result = []
        for obj in Devices.objects.all():
            devices.append({
                'device_type': model_to_dict(obj)['device_type'],
                'ip': model_to_dict(obj)['ip_add'],
                'username': request.user.username,
                'password': request.user.dev_password,
                'model': model_to_dict(obj)['model'],
                })
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cmd_output = run_parallel_session(
                devices,
                json.loads(form.cleaned_data['commands']),
                request,
                form.cleaned_data['cfg_cmd']
            )
            # redirect to a new URL:
            for text_line in cmd_output:
                if text_line:
                    result.append(text_line)
            cache.set('cmd_output', '\n'.join(result), 3600)
            return render(request, template, {'form': form, 'save_file': True})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommandsForm()

    return render(request, template, {'form': form})
