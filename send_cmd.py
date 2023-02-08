import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor as Tpe
from datetime import datetime
from itertools import repeat
from file_csv import get_cred

sys.path.append("/Users/netzen/study/BulkConfTool/netmiko/")

from netmiko import (ConnectHandler, NetmikoAuthenticationException,
                     NetmikoTimeoutException)

logging.getLogger("paramiko").setLevel(logging.INFO)

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
    start_msg = "===> {} Connection: {}"
    received_msg = "<=== {} Received:   {}"
    logging.info(start_msg.format(datetime.now().time(), devices["ip"]))
    try:
        with ConnectHandler(**devices) as net_connect:
            if cmd_type == "config":
                net_connect.config_mode()
                for cmd in commands[model]:
                    if r"local-user.*?privilege level \d*" in cmd:
                        cmd_show.append(
                            net_connect.send_command(
                                cmd,
                                expect_string=r"\[Y\/N\]$",
                                strip_command=False
                            )
                        )
                        cmd_show.append(
                            net_connect.send_command("Y", strip_command=False)
                        )
                    if r"super password level \d* cipher" in cmd:
                        cmd_show.append(
                            net_connect.send_command(
                                cmd,
                                expect_string=r"Enter Password\(<8-16>\):",
                                strip_command=False,
                            )
                        )
                        cmd_show.append(
                            net_connect.send_command(
                                PASSWORD,
                                expect_string=r"Confirm password:",
                                strip_command=False,
                            )
                        )
                        cmd_show.append(
                            net_connect.send_command(
                                ENABLE,
                                expect_string=r"\[.*?\]",
                                strip_command=False
                            )
                        )
                    cmd_show.append(
                        net_connect.send_command(
                            cmd, expect_string=r"\[.*?\]", strip_command=False
                        )
                    )
                    logging.info(f"output command {cmd_show}")
                if model == "nem6":
                    net_connect.commit()
                net_connect.save_config()
            if cmd_type == "show":
                for command in commands[model]:
                    cmd_show.append(net_connect.send_command(command))
            send_cmd = " ".join(cmd_show)
            logging.info(received_msg.format(
                datetime.now().time(), devices["ip"])
            )
            return f"""{"*"* 20} {devices["ip"]} {"*"* 20}\n\n
                   {send_cmd}\n\n"""
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
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
        "nem6": [
            "info-center loghost 172.16.155.200 facility local6",
            "undo info-center loghost 172.16.155.101",
        ],
        "ar6120": [
            "sysname ar1777v",
            "aaa",
            f"local-user test_user13 password irreversible-cipher {PASSWORD}",
            "local-user test_user13 service-type ssh",
            "local-user test_user13 privilege level 1",
        ],
        "2901": ["no logging 172.16.144.77", "logging 172.16.144.200"],
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
