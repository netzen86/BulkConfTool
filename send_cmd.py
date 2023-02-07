import os
import sys
import logging
from concurrent.futures import ThreadPoolExecutor as Tpe
from datetime import datetime
from itertools import repeat
from file_csv import get_cred


sys.path.append('/home/netzen/Study/netmiko/')

from netmiko import (ConnectHandler, NetmikoAuthenticationException,
                     NetmikoTimeoutException)


logging.getLogger("paramiko").setLevel(logging.INFO)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s",
    level=logging.INFO
)

PASSWORD = os.getenv('password')
ENABLE = os.getenv('en_pass')


def send_cmd(devices, commands, cmd_type):
    """Function for send command on network device"""
    cmd_show = []
    send_cmd = ''
    model = devices['model']
    del devices['model']
    start_msg = "===> {} Connection: {}"
    received_msg = "<=== {} Received:   {}"
    logging.info(start_msg.format(datetime.now().time(), devices["ip"]))
    try:
        with ConnectHandler(**devices) as net_connect:
            if cmd_type == 'config':
                net_connect.config_mode()
                for cmd in commands[model]:
                    logging.info(f'command {type(cmd)}')
                    if type(cmd) == list:
                        cmd_show.append(net_connect.send_multiline(cmd, strip_command=False))
                    cmd_show.append(net_connect.send_command(cmd, expect_string=r'\[.*?\]', strip_command=False))
                    logging.info(f'output command {cmd_show}')
                if model == 'nem6':
                    net_connect.commit()
                net_connect.save_config()
            if cmd_type == 'show':
                for command in commands[model]:
                    cmd_show.append(net_connect.send_command(command))
            send_cmd = " ".join(cmd_show)
            logging.info(received_msg.format(
                datetime.now().time(), devices["ip"])
            )
            return f'''{"*"* 20} {devices["ip"]} {"*"* 20}\n\n
                   {send_cmd}\n\n'''
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        return f'''{"*"* 20} {devices["ip"]} {"*"* 20}\n\n
               !!! ERROR !!!\n\n{error}'''


def run_parallel_session(devices, filename, commands, cmd_type='show', limit=3):
    """Function for run many connection to network devices"""
    with Tpe(max_workers=limit) as executor:
        result = executor.map(
            send_cmd, devices,
            repeat(commands),
            repeat(cmd_type)
        )
    with open(filename, "w") as f:
        f.writelines(result)


if __name__ == "__main__":
    config_conf = {
        'nem6': [
            'info-center loghost 172.16.155.200 facility local6',
            'undo info-center loghost 172.16.155.101',
        ],
        'ar6120': ['sysname ar1000v',
            [['super password level 15 cipher', r'Enter Password\(<8-16>\):'],
             [f'{ENABLE}\n', r'Confirm password:'],
             [f'{ENABLE}\n', '']],
            'aaa',
            f'local-user test_user777 password irreversible-cipher {PASSWORD}',
            'local-user test_user777 service-type ssh',
            [['local-user test_user777 privilege level 15', r'Warning: This operation may affect online users, are you sure to change the user privilege level ?[Y/N]'],
             ['y', '']]],
        '2901': ['no logging 172.16.144.77', 'logging 172.16.144.200'],
    }
    config_show = {
        'huawei': [
            'display cur'
        ],
        'huawei_vrpv8': [
            'display cur'
        ],
        'cisco_ios': [
            'show run'
            ],
    }
    run_parallel_session(
        get_cred('device.csv'),
        'output_cmd.txt',
        config_conf,
        cmd_type='config',
    )
