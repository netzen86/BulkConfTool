from inventory.models import Devices
from .models import Vlans, SwitchPortMgmt
from django import forms


class SwitchPortSearchForm(forms.Form):
    search_box = forms.CharField(max_length=100)
    # cleaned_data = {}


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

    # def clean(self):
    #     for value, key in self.instance:
    #         print(f' Data in validators: Value:{value} Key:{type(key)}')
    #         # self.cleaned_data[key] = value
    #     # Get the user submitted names from the cleaned_data dictionary
    #     return self.cleaned_data

    # def cleaned_data(self):
    #     return self.cleaned_data

    class Meta:
        model = SwitchPortMgmt
        fields = (
            'switch',
            'port',
            'socket',
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
            'switch': forms.TextInput(attrs={'readonly': True, 'size': 15}),
            'port': forms.TextInput(attrs={'readonly': True, 'size': 6}),
            'socket': forms.TextInput(attrs={'size': 7}),
            'description': forms.TextInput(attrs={'size': 15}),
            'mac': forms.TextInput(attrs={'size': 17}),
            'change_vlan': forms.TextInput(attrs={'size': 15}),
            'shut_port': forms.CheckboxInput(attrs={'size': 5}),
            'clear_mac': forms.CheckboxInput(attrs={'size': 5}),
            'state': forms.TextInput(attrs={'readonly': False, 'size': 6}),
            'on_off': forms.TextInput(attrs={'readonly': False, 'size': 3}),
            'connect': forms.TextInput(attrs={'readonly': False, 'size': 3}),
        }
