import logging
from concurrent.futures import ThreadPoolExecutor as Tpe
from datetime import datetime
from itertools import repeat

import sys
sys.path.append(('/home/netzen/Study/netmiko/'))

from netmiko import (ConnectHandler, NetmikoAuthenticationException,
                                NetmikoTimeoutException)

from file_csv import get_cred

logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s",
    level=logging.INFO
)


def conf_device(devices, commands):
    """Function for send command on network device"""
    start_msg = "===> {} Connection: {}"
    received_msg = "<=== {} Received:   {}"
    logging.info(start_msg.format(datetime.now().time(), devices["ip"]))
    try:
        with ConnectHandler(**devices) as net_connect:
            send_cmd = net_connect.send_config_set(
                commands[devices["device_type"]]
            )
            if devices['device_type'] == 'huawei_vrpv8':
                net_connect.commit()
            save_conf = net_connect.save_config()
            logging.info(received_msg.format(
                datetime.now().time(), devices["ip"])
            )
            return f'''{"*"* 20} {devices["ip"]} {"*"* 20}\n\n
                   {send_cmd}\n{save_conf}\n\n'''
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        return f'''{"*"* 20} {devices["ip"]} {"*"* 20}\n\n
               !!! ERROR !!!\n\n{error}'''


def run_parallel_session(devices, filename, commands, limit=3):
    """Function for run many connection to network devices"""
    with Tpe(max_workers=limit) as executor:
        result = executor.map(conf_device, devices, repeat(commands))
    with open(filename, "w") as f:
        f.writelines(result)


if __name__ == "__main__":
    config = {
        'huawei': [
            'info-center loghost 172.16.155.101 facility local6',
            'undo info-center loghost 172.16.155.100',
        ],
        'huawei_vrpv8': [
            'info-center loghost 172.16.155.102 level informational',
            'undo info-center loghost 172.16.155.100',
        ],
        'cisco_ios': ['no logging 172.16.144.66', 'logging 172.16.144.77'],
    }
    run_parallel_session(get_cred("device.csv"), "output_cmd.txt", config)
