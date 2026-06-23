from lib.interactive_session import InteractiveSession


def is_powered() -> bool:
    out = InteractiveSession().run("show")
    return "Powered: yes" in out


def is_paired(device_mac: str) -> bool:
    out = InteractiveSession().run(f"info {device_mac}")
    return "Paired: yes" in out


def is_connected(device_mac: str) -> bool:
    out = InteractiveSession().run(f"info {device_mac}")
    return "Connected: yes" in out
