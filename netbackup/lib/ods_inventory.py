import logging
from typing import Any, Dict, Type
from nornir import InitNornir
from nornir.core.inventory import Inventory
from nornir.core.filter import F
from nornir.core.plugins.inventory import InventoryPluginRegister
import pprint
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

from nornir.core.inventory import (
    Inventory,
    Group,
    Groups,
    Host,
    Hosts,
    Defaults,
    ConnectionOptions,
    HostOrGroup,
    ParentGroups,
)

logger = logging.getLogger(__name__)


def _get_connection_options(data: Dict[str, Any]) -> Dict[str, ConnectionOptions]:
    cp = {}
    for cn, c in data.items():
        cp[cn] = ConnectionOptions(
            hostname=c.get("hostname"),
            port=c.get("port"),
            username=c.get("username"),
            password=c.get("password"),
            platform=c.get("platform"),
            extras=c.get("extras"),
        )
    return cp

def _get_defaults(data: Dict[str, Any]) -> Defaults:
    return Defaults(
        hostname=data.get("hostname"),
        port=data.get("port"),
        username=data.get("username"),
        password=data.get("password"),
        platform=data.get("platform"),
        data=data.get("data"),
        connection_options=_get_connection_options(data.get("connection_options", {})),
    )


def _get_inventory_element(
    typ: Type[HostOrGroup], data: Dict[str, Any], name: str, defaults: Defaults
) -> HostOrGroup:
    return typ(
        name=name,
        hostname=data.get("hostname"),
        port=data.get("port"),
        username=data.get("username"),
        password=data.get("password"),
        platform=data.get("platform"),
        data=data.get("data"),
        groups=data.get(
            "groups"
        ),  # this is a hack, we will convert it later to the correct type
        defaults=defaults,
        connection_options=_get_connection_options(data.get("connection_options", {})),
    )


class OdsDictInventory:
    def __init__(
        self,
        hosts_dict: dict,
        groups_dict: dict,
        defaults_dict: dict,
    ) -> None:
        """
        SimpleInventory is an inventory plugin that loads data from YAML files.
        The YAML files follow the same structure as the native objects
        Args:
          host_file: path to file with hosts definition
          group_file: path to file with groups definition. If
                it doesn't exist it will be skipped
          defaults_file: path to file with defaults definition.
                If it doesn't exist it will be skipped
        """

        self.hosts_dict = hosts_dict
        self.groups_dict = groups_dict
        self.defaults_dict = defaults_dict

    def load(self) -> Inventory:

        if len(self.defaults_dict) > 0:
            defaults = _get_defaults(self.defaults_dict)
        else:
            defaults = Defaults()

        hosts = Hosts()

        for n, h in self.hosts_dict.items():
            hosts[n] = _get_inventory_element(Host, h, n, defaults)

        groups = Groups()
        if len(self.groups_dict) > 0:
            for n, g in self.groups_dict.items():
                groups[n] = _get_inventory_element(Group, g, n, defaults)

            for h in hosts.values():
                h.groups = ParentGroups([groups[g] for g in h.groups])

            for g in groups.values():
                g.groups = ParentGroups([groups[g] for g in g.groups])

        return Inventory(hosts=hosts, groups=groups, defaults=defaults)
