from django import forms

CMD_TMPLATE = '''Для отправки команд на устройства нужно
                 заполнить шаблон:
                 {"huawei": ["cmd 1", "cmd 2", ... ],
                 "huawei_vrpv8": [], "cisco_ios": []}'''


class CommandsForm(forms.Form):
    commands = forms.CharField(
        widget=forms.Textarea,
        label='commands',
        help_text=CMD_TMPLATE
    )
