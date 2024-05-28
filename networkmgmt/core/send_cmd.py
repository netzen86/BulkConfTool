import logging
# import sys
from django.contrib import messages
from concurrent.futures import ThreadPoolExecutor as Tpe
from datetime import datetime
from itertools import repeat
from paramiko import ssh_exception

# sys.path.append("../netmiko/")


from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException
    )

# from .file_csv import get_cred

logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s",
    level=logging.INFO
)


def send_cmd(devices, commands, request, cmd_type):
    """Function for send command on network device"""
    cmd_show = []
    send_cmd = ""
    model = devices["model"]
    del devices["model"]
    start_msg = "===> {} Connection: {}"
    received_msg = "<=== {} Received:   {}"
    error_msg = "!!! {}  Error:  {}"
    logging.info(start_msg.format(datetime.now().time(), devices["ip"]))
    messages.add_message(
        request,
        messages.INFO,
        start_msg.format(datetime.now().time(), devices["ip"])
    )
    try:
        with ConnectHandler(**devices) as net_connect:
            if cmd_type:
                net_connect.config_mode()
                for cmd in commands[model]:
                    if type(cmd) is list:
                        cmd_show.append(
                            net_connect.send_multiline(cmd, cmd_verify=False)
                        )
                    else:
                        logging.info(f'in else {model}')
                        cmd_show.append(
                            net_connect.send_command(
                                cmd, expect_string=r"\[?.*?[\]#]",
                                strip_command=False
                            )
                        )
                if model == "huawei_vrpv8":
                    net_connect.commit()
                net_connect.save_config()
            if not cmd_type:
                for command in commands[devices['device_type']]:
                    cmd_show.append(net_connect.send_command(command))
                send_cmd = " ".join(cmd_show)
            logging.info(received_msg.format(
                datetime.now().time(), devices["ip"])
            )
            messages.add_message(
                request,
                messages.INFO,
                received_msg.format(datetime.now().time(), devices["ip"])
            )
            return f'''{"*"* 20} {devices["ip"]} {"*"* 20}\n\n
                   {send_cmd}\n\n'''
    except (NetmikoTimeoutException,
            NetmikoAuthenticationException,
            ssh_exception.SSHException) as error_exc:
        error = f'''{"*"* 20} {devices["ip"]} {"*"* 20}\n\n
               !!! ERROR !!!\n\n{error_exc}'''
        logging.info(error_msg.format(datetime.now().time(), error))
        messages.add_message(
            request,
            messages.INFO,
            received_msg.format(datetime.now().time(),
                                f'{devices["ip"]} {error_exc}'))
        return error


def run_parallel_session(
    devices,
    commands,
    request,
    cmd_type=False,
    limit=3
):
    """Function for run many connection to network devices"""
    with Tpe(max_workers=limit) as executor:
        result = executor.map(
            send_cmd, devices,
            repeat(commands),
            repeat(request),
            repeat(cmd_type),
        )
    return result
