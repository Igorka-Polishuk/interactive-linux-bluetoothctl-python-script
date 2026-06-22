import re

mac_address_re = r"\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b"
device_name_re = r"\[NEW\]\s+Device\s+(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\s+(.+)$"


def get_all_device_mac_addresses(input_str: str) -> list[str]:
    return re.findall(mac_address_re, input_str)


def get_all_device_names(input_str: str) -> list[str]:
    return re.findall(device_name_re, input_str)


def show_all_devices():
    pass
