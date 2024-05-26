# import sys
# sys.path.append("../netmiko/")

from netmiko.ssh_dispatcher import CLASS_MAPPER_BASE


def keys_to_tup(dictionary=CLASS_MAPPER_BASE):
    result_tuple = []
    for key in dictionary.keys():
        result_tuple.append(tuple([key, key]))
    return tuple(result_tuple)
