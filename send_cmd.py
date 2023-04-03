import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor as Tpe
from datetime import datetime
from itertools import repeat
from file_csv import get_cred
from paramiko import ssh_exception

sys.path.append("/Users/netzen/study/BulkConfTool/netmiko/")

from netmiko import (ConnectHandler, NetmikoAuthenticationException,
                     NetmikoTimeoutException)

logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format="%(threadName)s %(name)s %(levelname)s: %(message)s",
    level=logging.INFO
)

PASSWORD = os.getenv("password")
ENABLE = os.getenv("en_pass")


def send_cmd(devices, commands, cmd_type):
    """Function for send command on network device"""
    cmd_show = []
    send_cmd = ""
    model = devices["model"]
    del devices["model"]
    start_msg = "===> {} Connection: {} {}"
    received_msg = "<=== {} Received:   {} {}"
    logging.info(start_msg.format(datetime.now().time(), devices["ip"], model))
    try:
        with ConnectHandler(**devices) as net_connect:
            if cmd_type == "config":
                net_connect.config_mode()
                for cmd in commands[model]:
                    if type(cmd) == list:
                        cmd_show.append(
                            net_connect.send_multiline(cmd, cmd_verify=False)
                        )
                    else:
                        cmd_show.append(
                            net_connect.send_command(
                                cmd, expect_string=r"\[?.*?[\]#]",
                                strip_command=False
                            )
                        )
                if model == "nem6&ce":
                    net_connect.commit()
                net_connect.save_config()
            if cmd_type == "show":
                for command in commands[model]:
                    cmd_show.append(net_connect.send_command(command))
            send_cmd = "\n".join(cmd_show)
            logging.info(received_msg.format(
                datetime.now().time(), devices["ip"], model)
            )
            return f"""{"*"* 20} {devices["ip"]} {"*"* 20}\n\n
                   {send_cmd}\n\n"""
    except (NetmikoTimeoutException, NetmikoAuthenticationException, ssh_exception.SSHException) as error:
        return f"""{"*"* 20} {devices["ip"]} {"*"* 20}\n\n
               !!! ERROR !!!\n\n{error}"""


def run_parallel_session(
    devices,
    filename,
    commands,
    cmd_type="show",
    limit=3
):
    """Function for run many connection to network devices"""
    with Tpe(max_workers=limit) as executor:
        result = executor.map(
            send_cmd,
            devices,
            repeat(commands),
            repeat(cmd_type)
        )
    with open(filename, "w") as f:
        f.writelines(result)


if __name__ == "__main__":
    config_conf = {
        "nem6&ce": [
            "sysname ne8888v",
            "aaa",
            f"local-user test_user177 password irreversible-cipher {PASSWORD}",
            "local-user test_user177 service-type ssh",
            "local-user test_user177 level 3",
        ],
        "ar6120": [
            [["super password level 15 cipher", r"Enter Password\(<8\-16>\):"],
             [f"{ENABLE}", r"Confirm password:"],
             [f"{ENABLE}", ""], ],
            "sysname ar6162v",
            "aaa",
            f"local-user test_user177 password irreversible-cipher {PASSWORD}",
            "local-user test_user177 service-type ssh",
            [["local-user test_user44 privilege level 1", r"[Y/N]"],
             ["y", ""], ],
        ],
        "cisco": [
            "hostname ciscorouter",
            f"username test-user177 priv 1 sec {PASSWORD}",
            f"enable sec {ENABLE}"],
    }
    config_show = {
        "huawei": ["display cur"],
        "huawei_vrpv8": ["display cur"],
        "cisco_ios": ["show run"],
    }
    run_parallel_session(
        get_cred("device.csv"),
        "output_cmd.txt",
        config_conf,
        cmd_type="config",
    )
