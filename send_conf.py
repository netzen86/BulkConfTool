import logging
from datetime import datetime
from netmiko import ConnectHandler
from file_csv import get_cred
from concurrent.futures import ThreadPoolExecutor as Tpe
from itertools import repeat


logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO
)


def conf_device(devices, commands):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    # msg = f"{devices} {commands}"
    logging.info(start_msg.format(datetime.now().time(), devices['ip']))
    with ConnectHandler(**devices) as net_connect:
        send_cmd = net_connect.send_config_set(
            commands[devices['device_type']]
        )
        save_conf = net_connect.save_config()
        logging.info(received_msg.format(datetime.now().time(), devices['ip']))
        return (
            f"{'*'* 20}{devices['ip']}{'*'* 20}\n\n{send_cmd}\n{save_conf}\n\n"
        )


def run_parallel_session(devices, filename, commands, limit=3):
    with Tpe(max_workers=limit) as executor:
        result = executor.map(conf_device, devices, repeat(commands))
    with open(filename, "w") as f:
        f.writelines(result)


if __name__ == "__main__":
    config = {
        'huawei': [
            'info-center loghost 172.16.155.99 level informational',
            'undo info-center loghost 172.16.155.88',
            'commit'
        ],
        'cisco_ios': [
            'no logging 172.16.144.55',
            'logging 172.16.144.66'
        ]
    }
    run_parallel_session(get_cred('device.csv'), "output_cmd.txt", config)