from django import forms
from .models import StartTime


class BackUpForm(forms.ModelForm):

    class Meta():
        model = StartTime
        fields = ('time', 'days')
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'days': forms.CheckboxSelectMultiple,
        }
        # widgets = {
        #     'date': forms.SelectDateWidget(
        #          empty_label=("Choose Year", "Choose Month", "Choose Day"),
        #     ),
        #     'time': forms.TimeInput(attrs={'type': 'time'}),
