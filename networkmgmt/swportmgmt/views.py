from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SwitchPortSearchForm, SwitchPortMgmtForm
from django.db.models import Q
from .models import SwitchPort, Vlans, SwitchPortMgmt
from django.forms import formset_factory
from inventory.models import Devices
from django import forms
from pprint import pprint


def get_port_socket(query):
    object_list = SwitchPort.objects.filter(
        Q(socket__icontains=query) | Q(description__icontains=query)
    )
    return object_list


@login_required(login_url='auth/login')
def switch_port_mgmt(request):
    """MGMT port switch"""
    port_socket = []
    template = 'swportmgmt/swportmgmt.html'
    form = SwitchPortSearchForm(
        request.POST or None,
    )
    if form.is_valid():
        for socket in get_port_socket(
            form.cleaned_data['search_box']
        ).values_list():
            port_socket.append({
                'switch': Devices.objects.get(pk=socket[2]).ip_add,
                'port': socket[3],
                'socket': socket[4],
                'description': socket[5],
            })
        SwitchPortFormSet = formset_factory(
            SwitchPortMgmtForm,
            extra=0,
        )
        formset = SwitchPortFormSet(initial=port_socket)
        return render(request, template, {
            'form': form,
            'messages': formset,
        })
    else:
        return render(request, template, {'form': form})
