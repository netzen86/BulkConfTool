'''
Для примера дописания функций в Netmiko
'''
import re
from netmiko.huawei.huawei import HuaweiVrpv8SSH, HuaweiBase
import logging

logging.basicConfig(filename='huawei.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


class Huaweis(HuaweiVrpv8SSH):
    def __init__(self, **device):
        super().__init__(**device)
        self.enable()

    def _check_error_in_command(self, cmd_output, cmd):
        regexp = r"Error: (.*)"
        err_msg_tmpl = (
            'При выполнении команды "{cmd}" на устройстве "{host}" '
            'возникла ошибка "{error}"'
        )
        if "Error: " in cmd_output:
            error = re.search(regexp, cmd_output)
            raise ErrorInCommand(err_msg_tmpl.format(
                cmd=cmd, host=self.host, error=error.group(1)))

    def save_config(self, cmd="save", confirm=True, confirm_response="y"):
        """ Save Config for HuaweiVrpv8SSH"""
        return HuaweiBase.save_config(
            self,
            cmd=cmd,
            confirm=confirm,
            confirm_response=confirm_response
            )

    def send_command(self, command_string, *params, **kwparams):
        out_cmd = super().send_command(command_string, *params, **kwparams)
        self._check_error_in_command(out_cmd, command_string)
        return out_cmd

    def send_config_set(
        self,
        config_commands=None,
        ignore_errors=False,
        *params,
        **kwparams
    ):
        converted_cfg_cmds = [config_commands]
        out_cmd = ""
        for cmd in converted_cfg_cmds:
            out_cmd += super().send_config_set(cmd)
            if not ignore_errors:
                self._check_error_in_command(out_cmd, cmd)
        return out_cmd
