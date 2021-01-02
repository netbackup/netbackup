"""Base connection class.
"""
from lib import constant
from lib.netmiko_driver import NetmikoDriver
from lib.scrapli_driver import ScrapliDriver


class Connection:
    """A connection class which is a wrapper arounf nornir which uses Netmiko or scrapli driver."""

    def __init__(self, conn_type: str) -> None:
        """Initialize connection.

        Args:
            conn_type (str): Type of connection possible options are NETMIKO or SCRAPLI
        """
        if conn_type == constant.NETMIKO:
            self.conn = NetmikoDriver()
        elif conn_type == constant.SCRAPLI:
            self.conn = ScrapliDriver()

    def open(self, hosts={}, groups={}, defaults={}) -> None:
        """Initialize nornir class.

        More info on schema of the dictionary can be found in below link
        https://nornir.readthedocs.io/en/latest/tutorial/inventory.html

        Args:
        
            hosts (dict): Host related information like IP, user and password.

            EX:
            {
                "host1": {
                "hostname": "100.100.0.10",
                "username": "admin",
                "password": "NttLtd2020",
                         }
            }

            groups (dict, optional): Defaults to {}.

            EX:
            Not Implemented yet leave to default.

            defaults (dict, optional): Connection driver parameters.

            EX:
              SCRAPLI:
              {
                "connection_options": {
                    "scrapli": {
                        "extras": {
                            "auth_strict_key": False,
                            "ssh_config_file": True,
                            "transport": "ssh2",
                        }
                    }
                }
            }

            or

               NETMIKO:
               {
                "connection_options": {
                    "netmiko": {
                        "extras": {"global_delay_factor": 2}
                    }
                }
            }
                

        """
        self.conn.open(hosts, groups, defaults)

    def close(self):
        self.conn.close()

    def send_command(self, command: str) -> dict:
        return self.conn.send_command(command)

    def get_prompt(self) -> None:
        return self.conn.get_prompt()
