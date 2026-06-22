from utils.constants import DEVICE_MAC
from lib.sys_interact import run


def is_powered() -> bool:
    out = run("show")
    return "Powered: yes" in out


def is_paired() -> bool:
    out = run(f"info {DEVICE_MAC}")
    return "Paired: yes" in out


def is_connected() -> bool:
    out = run(f"info {DEVICE_MAC}")
    return "Connected: yes" in out
