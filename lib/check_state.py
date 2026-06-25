from lib.interactive_session import run


def is_powered() -> bool:
    out = run("show")
    return "Powered: yes" in out


def is_paired(device_mac: str) -> bool:
    out = run(f"info {device_mac}")
    return "Paired: yes" in out


def is_connected(device_mac: str) -> bool:
    out = run(f"info {device_mac}")
    return "Connected: yes" in out
