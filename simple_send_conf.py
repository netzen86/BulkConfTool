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
    msg = f"{devices} {commands}"
    logging.info(start_msg.format(datetime.now().time(), msg))
    with ConnectHandler(**devices) as net_connect:
        res_cmd = net_connect.send_config_set(commands)
        write_memo = net_connect.save_config()
        logging.info(received_msg.format(datetime.now().time(),
                     f'{res_cmd}, {write_memo}'))
        return res_cmd, write_memo


def run_parallel_session(devices, filename, commands, limit=3):
    with Tpe(max_workers=limit) as executor:
        result = executor.map(conf_device, devices, repeat(commands))
    with open(filename, "w") as f:
        f.writelines(*result)


if __name__ == "__main__":
    config = [
        'info-center loghost 172.16.155.99 level informational',
        'undo info-center loghost 172.16.155.88',
        # 'local-user user363 password irreversible-cipher password',
        'commit'
        ]
    run_parallel_session(get_cred('device.csv'), 'conf_out.txt', config)
