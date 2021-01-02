from nornir_netmiko import netmiko_send_command
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister
from lib.ods_inventory import OdsDictInventory
from lib.constant import NETMIKO_EXTRAS


class NetmikoDriver:
    def __init__(self):
        InventoryPluginRegister.register("OdsDictInventory", OdsDictInventory)
        self.nr = None

    def open(self, hosts_dict, groups_dict, defaults_dict):
        if len(defaults_dict) == 0:
            defaults_dict = NETMIKO_EXTRAS
        else:
            defaults_dict.update(NETMIKO_EXTRAS)

        self.nr = InitNornir(
            runner={
                "plugin": "threaded",
                "options": {
                    "num_workers": 1,
                },
            },
            inventory={
                "plugin": "OdsDictInventory",
                "options": {
                    "hosts_dict": hosts_dict,
                    "groups_dict": groups_dict,
                    "defaults_dict": defaults_dict,
                },
            },
        )
        print("Netmiko-open")
        return self.nr

    def close(self):
        print("Netmiko-close")
        self.nr.close_connections()

    def send_command(self, command: str) -> dict:
        """Send command and return results.
        Args:
            command (str): Command to run on device.
        """
        print("Netmiko-send_command")
        result = self.nr.run(task=netmiko_send_command, command_string=command)
        return result
