from django import forms


class BackUpForm(forms.Form):
    date_time = forms.CharField(
        widget=forms.DateTimeInput,
        label='Команды для выполнения',
    )
