SCRAPLI = "SCRAPLI"
NETMIKO = "NETMIKO"
PLATFORMCONVERT = {
    "cisco_ios": "cisco_iosxe",
    "cisco_nxos": "cisco_nxos",
    "cisco_xr": "cisco_iosxr",
    "arista_eos": "arista_eos",
    "juniper_junos": "juniper_junos",
}
SCRAPLI_EXTRAS = {
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
NETMIKO_EXTRAS = {
    "connection_options": {"netmiko": {"extras": {"global_delay_factor": 2}}}
}

RUNNER = {
    "plugin": "threaded",
    "options": {
        "num_workers": 1,
    },
}
