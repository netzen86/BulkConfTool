from huawei import Huaweis
from file_csv import get_cred
from concurrent.futures import ThreadPoolExecutor as Tpe
from itertools import repeat


def conf_device(devices, commands):
    print(devices, commands)
    with Huaweis(**get_cred(devices)) as net_connect:
        res_cmd = net_connect.send_config_set(commands, ignore_errors=False)
        print(res_cmd)
        write_memo = net_connect.save_config()
        print(write_memo)
        return res_cmd, write_memo


def run_parallel_session(devices, filename, commands, limit=3):
    with Tpe(max_workers=limit) as executor:
        result = executor.map(conf_device, devices, repeat(commands))
    with open(filename, "w") as f:
        f.writelines(*result)


if __name__ == "__main__":
    config = [
        'info-center loghost 172.16.155.18 level informational',
        'undo info-center loghost 172.16.155.17',
        # 'local-user user363 password irreversible-cipher password',
        'commit'
        ]
    run_parallel_session(['device.csv'], 'show_out_19.4.txt', config)
