import sys
import csv
import os
from pprint import pprint


path_to_file = sys.argv[1]
result = []


commands_dic = {
    'no service pad': '-',
    'service password-encryption': '-',
    'no service dhcp': '-',
    'ip dhcp bootp ignore': '-',
    'no ip http server': '-',
    'no ip http secure-server': '-',
    'snmp-server community public RO 1': '-',
    'ntp server 192.168.1.1': '-',
    'logging trap notifications': '-',
    'logging 192.168.1.1': '-',
    'logging 192.168.1.2': '-',
    'aaa authentication login default group tacacs+ local': '-',
    'aaa authorization config-commands': '-',
    'aaa authorization exec default group tacacs+ none': '-',
    'aaa authorization commands 1 default group tacacs+ none': '-',
    'aaa authorization commands 15 default group tacacs+ none': '-',
    'aaa accounting exec default start-stop group tacacs+': '-',
    'aaa accounting commands 0 default start-stop group tacacs+': '-',
    'aaa accounting commands 1 default start-stop group tacacs+': '-',
    'aaa accounting commands 15 default start-stop group tacacs+': '-',
}


def parse_conf_aaa(file, conf_dict):
    config = []
    hosname = ''
    result = []
    with open(file) as f:
        for line in f:
            if line:
                if line.startswith('hostname'):
                    _, hosname = line.split(' ')
                config.append(line.rstrip('\n'))
        for command in conf_dict.keys():
            for cmd in config:
                if cmd.strip() in conf_dict.keys():
                    conf_dict[cmd.strip()] = '+'
        for key, item in conf_dict.items():
            result.append([hosname.rstrip('\n'), key, item])
    return result


if os.path.isdir(path_to_file):
    for file in os.listdir(path_to_file):
        if os.path.isfile(path_to_file + file):
            result.append(
                parse_conf_aaa(
                    path_to_file + file, commands_dic.copy()))

else:
    if os.path.isfile(path_to_file):
        result.append(parse_conf_aaa(path_to_file, commands_dic.copy()))


pprint(result)

with open('conf_aaa.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['hostname', 'command', 'in config'])
    for rows in result:
        for row in rows:
            writer.writerow(row)
