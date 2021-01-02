from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister
from lib.ods_inventory import OdsDictInventory
from lib.constant import PLATFORMCONVERT, SCRAPLI_EXTRAS, RUNNER
from nornir_scrapli.tasks import get_prompt, send_command, send_configs


class ScrapliDriver:
    def __init__(self):
        InventoryPluginRegister.register("OdsDictInventory", OdsDictInventory)
        self.nr = None

    def open(self, hosts_dict, groups_dict, defaults_dict):
        defaults_dict.update(SCRAPLI_EXTRAS)
        if len(defaults_dict) != 0:
            defaults_dict = self._replace_scrapli_platform(defaults_dict)

        self.nr = InitNornir(
            runner=RUNNER,
            inventory={
                "plugin": "OdsDictInventory",
                "options": {
                    "hosts_dict": hosts_dict,
                    "groups_dict": groups_dict,
                    "defaults_dict": defaults_dict,
                },
            },
        )
        print("Scrapli-open")
        return self.nr

    def _replace_scrapli_platform(self, hosts_dict):
        if "name" not in hosts_dict:
            if "platform" in hosts_dict:
                if hosts_dict["platform"] in PLATFORMCONVERT:
                    hosts_dict["platform"] = PLATFORMCONVERT[hosts_dict["platform"]]
            if "connection_options" in hosts_dict:
                if "platform" in hosts_dict["connection_options"]["scrapli"]:
                    if (
                        hosts_dict["connection_options"]["scrapli"]["platform"]
                        in PLATFORMCONVERT
                    ):
                        print(
                            PLATFORMCONVERT[
                                hosts_dict["connection_options"]["scrapli"]["platform"]
                            ]
                        )
                        hosts_dict["connection_options"]["scrapli"][
                            "platform"
                        ] = PLATFORMCONVERT[
                            hosts_dict["connection_options"]["scrapli"]["platform"]
                        ]
        else:
            for host in hosts_dict:
                if "platform" in hosts_dict[host]:
                    if hosts_dict[host]["platform"] in PLATFORMCONVERT:
                        hosts_dict[host]["platform"] = PLATFORMCONVERT[
                            hosts_dict[host]["platform"]
                        ]
                if "connection_options" in hosts_dict[host]:
                    if "platform" in hosts_dict[host]["connection_options"]["scrapli"]:
                        if (
                            hosts_dict[host]["connection_options"]["scrapli"][
                                "platform"
                            ]
                            in PLATFORMCONVERT
                        ):
                            print(
                                PLATFORMCONVERT[
                                    hosts_dict[host]["connection_options"]["scrapli"][
                                        "platform"
                                    ]
                                ]
                            )
                            hosts_dict[host]["connection_options"]["scrapli"][
                                "platform"
                            ] = PLATFORMCONVERT[
                                hosts_dict[host]["connection_options"]["scrapli"][
                                    "platform"
                                ]
                            ]
        return hosts_dict

    def close(self):
        print("Scrapli-close")
        self.nr.close_connections()

    def send_command(self, command: str) -> dict:
        """Send command and return results.
        Args:
            command (str): Command to run on device.
        """
        print("Scrapli-send_command")
        result = self.nr.run(task=send_command, command=command)
        return result

    def get_prompt(self) -> None:
        """Gets the prompt of the device.
        """
        return nr.run(task=get_prompt)
