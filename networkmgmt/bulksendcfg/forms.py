from django import forms

HLP_TEXT = 'Для отправки команд на устройства нужно заполнить шаблон.'
CMD_DICT_TMPLATE = '''{"huawei": ["disp ver", "disp ip int b"], "huawei_vrpv8": ["disp ver"], "cisco_ios": ["sh ver"]}'''


class CommandsForm(forms.Form):
    commands = forms.CharField(
        widget=forms.Textarea,
        label='Команды для выполнения',
        help_text=HLP_TEXT,
        initial=CMD_DICT_TMPLATE
    )
    cfg_cmd = forms.BooleanField(
        label='Команды конфигурации',
        initial=False,
        required=False
    )
