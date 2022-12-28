import logging
from concurrent.futures import ThreadPoolExecutor as Tpe
from datetime import datetime
from itertools import repeat

from netmiko import (ConnectHandler, NetmikoAuthenticationException,
                     NetmikoTimeoutException)

from file_csv import get_cred

logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s",
    level=logging.INFO
)


def send_cmd(devices, commands, cmd_type):
    """Function for send command on network device"""
    cmd_show = []
    start_msg = "===> {} Connection: {}"
    received_msg = "<=== {} Received:   {}"
    logging.info(start_msg.format(datetime.now().time(), devices["ip"]))
    try:
        with ConnectHandler(**devices) as net_connect:
            if cmd_type == 'config':
                send_cmd = net_connect.send_config_set(
                    commands[devices['device_type']]
                )
                if devices['device_type'] == 'huawei_vrpv8':
                    net_connect.commit()
                    net_connect.save_config()
            if cmd_type == 'show':
                for command in commands[devices['device_type']]:
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
        'huawei': [
            'info-center loghost 172.16.155.200 facility local6',
            'undo info-center loghost 172.16.155.101',
        ],
        'huawei_vrpv8': [
            'info-center loghost 172.16.155.200 level informational',
            'undo info-center loghost 172.16.155.101',
        ],
        'cisco_ios': ['no logging 172.16.144.77', 'logging 172.16.144.200'],
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
        config_show
    )
