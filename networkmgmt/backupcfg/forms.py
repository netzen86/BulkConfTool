from django import forms


class BackUpForm(forms.Form):
    forms.TimeField(
        label='Введите время',
    )
