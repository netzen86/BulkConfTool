from inventory.models import Devices
from .models import Vlans, SwitchPortMgmt
from django import forms


class SwitchPortSearchForm(forms.Form):
    search_box = forms.CharField(max_length=100)


class SwitchPortMgmtForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SwitchPortMgmtForm, self).__init__(*args, **kwargs)
        if kwargs.get('initial'):
            self.fields['change_vlan'] = forms.ModelChoiceField(
                queryset=Vlans.objects.filter(
                    switch_id=Devices.objects.get(
                        ip_add=kwargs.get('initial')['switch'])
                )
            )

    class Meta:
        model = SwitchPortMgmt
        fields = (
            'switch',
            'port',
            'description',
            'mac',
            'change_vlan',
            'shut_port',
            'clear_mac',
            'state',
            'on_off',
            'connect',
        )
        widgets = {
            'switch': forms.TextInput(attrs={'disabled': True, 'size': 15}),
            'port': forms.TextInput(attrs={'disabled': True, 'size': 6}),
            'description': forms.TextInput(attrs={'disabled': True, 'size': 15}),
        }
