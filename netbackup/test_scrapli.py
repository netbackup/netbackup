hosts_dict = {
    "cisco3": {
        "hostname": "100.100.0.10",
        "username": "admin",
        "password": "NttLtd2020",
        "connection_options": {
            "scrapli": {
                "extras": {
                    "auth_strict_key": False,
                    "ssh_config_file": True,
                    "transport": "ssh2",
                },
                "hostname": "100.100.0.10",
                "password": "NttLtd2020",
                "platform": "cisco_iosxe",
                "port": 22,
                "username": "admin",
            }
        },
    }
}

groups_dict = {
    "cisco": {
        "platform": "ios",
    },
    "arista": {"platform": "eos"},
    "juniper": {"platform": "junos"},
}

defaults_dict = {
    "username": "pyclass",
    "password": "password",
    "data": {"key3": "value3"},
}

from lib.connection import Connection
from lib.constant import SCRAPLI

command = "show version"
import datetime

a = datetime.datetime.now()

conn = Connection(SCRAPLI)
conn.open(hosts_dict, groups_dict, defaults_dict)
result_dt = conn.send_command(command)
print(result_dt["cisco3"].result)
conn.close()

b = datetime.datetime.now()
c = b - a
print("Executation time", SCRAPLI, c.seconds)
