from django import forms
from .models import StartTime


class BackUpForm(forms.ModelForm):

    class Meta():
        model = StartTime
        fields = ('date', 'time')

        widgets = {
            'date': forms.SelectDateWidget(
                 empty_label=("Choose Year", "Choose Month", "Choose Day"),
            ),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
