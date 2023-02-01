from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SwitchPortSearchForm, SwitchPortMgmtForm
from django.db.models import Q
from .models import SwitchPort, Vlans, SwitchPortMgmt
from django.forms import formset_factory
from inventory.models import Devices
from django import forms
from pprint import pprint
from django.views.generic.base import TemplateView


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


def _get_form(request, formcls, prefix):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix)


class SwitchPortMgmtView(TemplateView):
    template_name = 'swportmgmt/swportmgmt.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {'form': SwitchPortSearchForm(), #prefix='form_pre'),
             'bform': SwitchPortMgmtForm(prefix='bform_pre')}
            )

    def post(self, request, *args, **kwargs):
        port_socket = []
        form = SwitchPortSearchForm(request.POST or None)
        # form = _get_form(request, SwitchPortSearchForm, 'SwitchPortSearchForm')
        #bform = SwitchPortMgmtForm(request.POST or None)
        bform = _get_form(request, SwitchPortMgmtForm, 'SwitchPortMgmtForm')
        if form.is_valid():
            # Process aform and render response
            print(form.cleaned_data)
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
                extra=0
            )
            bform = SwitchPortFormSet(initial=port_socket)
        elif bform.is_valid():
            # Process bform and render response
            print(form.cleaned_data)
        return self.render_to_response({'form': form, 'messages': bform})
