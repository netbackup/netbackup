hosts_dict = {"cisco3": {"hostname": "100.100.0.10"}}

defaults_dict = {
    "username": "admin",
    "password": "NttLtd2020",
    "port": 22,
    "platform": "cisco_ios"
}

from lib.connection import Connection
from lib.constant import NETMIKO
from lib.constant import SCRAPLI

command = "show version"

import timeit


# conn = Connection(NETMIKO)
# conn.open(hosts=hosts_dict, defaults=defaults_dict)
# result_dt = conn.send_command(command)
# print(result_dt["cisco3"].result)
# conn.close()

conn1 = Connection(NETMIKO)
conn1.open(hosts=hosts_dict, defaults=defaults_dict)
result_dt = conn1.send_command(command)
print(result_dt["cisco3"].result)
conn1.close()
