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
from django.views.generic.edit import FormView


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


class MainView(TemplateView):
    template_name = 'swportmgmt/swportmgmttest.html'

    def get(self, request, *args, **kwargs):
        search_form = SwitchPortSearchForm(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['search_form'] = search_form
        return self.render_to_response(context)


class SwitchPortSearchFormView(FormView):
    form_class = SwitchPortSearchForm
    template_name = 'swportmgmt/swportmgmttest.html'

    def post(self, request, *args, **kwargs):
        port_socket = []
        search_form = self.form_class(request.POST)
        switchportmgmt_form = SwitchPortMgmtForm(self.request.GET or None)
        if search_form.is_valid():
            for socket in get_port_socket(
                search_form.cleaned_data['search_box']
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
            switchportmgmt_form = SwitchPortFormSet(initial=port_socket)

            return self.render_to_response(
                {'search_form': search_form,
                 'switchportmgmt': switchportmgmt_form}
                )
        else:
            return self.render_to_response(
                self.get_context_data(
                    search_form=search_form
                ))


class SwitchPortMgmtFormView(FormView):
    form_class = SwitchPortMgmtForm
    template_name = 'swportmgmt/swportmgmttest.html'

    def post(self, request, *args, **kwargs):
        switchportmgmt_form = self.form_class(request.POST)
        search_form = SwitchPortSearchForm(self.request.GET or None)
        print(f'!!! DATA {switchportmgmt_form.data}')
        # switchportmgmt_form.clean()
        # print(f'!!! Instance {switchportmgmt_form.errors}')
        if switchportmgmt_form.is_valid():
            print('!!! This fucking form valid !!!')
            return self.render_to_response(
                {'search_form': search_form,
                 'switchportmgmt': switchportmgmt_form}
                )
        else:
            return self.render_to_response(
                self.get_context_data(
                    search_form=search_form,
                    switchportmgmt_form=switchportmgmt_form
                )
            )
