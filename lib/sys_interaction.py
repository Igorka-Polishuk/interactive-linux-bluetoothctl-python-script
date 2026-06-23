import subprocess
import getpass
import sys
import re
import time

from lib.check_state import is_connected
from lib.interactive_session import InteractiveSession
from lib.constants import CONNECT_TIMEOUT


def start_bluetoothctl_service() -> bool:
    unblock_hardware_result = subprocess.run(
        ["rfkill", "unblock", "bluetooth"], capture_output=True
    )
    if not unblock_hardware_result.stdout:
        password = getpass.getpass("sudo password: ")
        result = subprocess.run(
            ["sudo", "-S", "systemctl", "start", "bluetooth"],
            input=password + "\n",
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("❌ Wrong password or permission denied")
            sys.exit(1)

        return True
    else:
        print("❌ Something went wrong")
        sys.exit(1)


def get_names_and_mac_addresses_of_devices(input_str: str):
    pattern = r"Device\s+([0-9A-F:]{17})\s+(.+)"

    matches = re.findall(pattern, input_str)

    mac_addresses = [mac for mac, _, in matches]
    device_names = [name.strip() for _, name, in matches]

    result = {}
    for i, mac_address in enumerate(mac_addresses):
        result[mac_address] = device_names[i]

    return result


def power_on():
    print("Enabling Bluetooth...")
    InteractiveSession().run("power on")
    time.sleep(1)


def connect_device(device_mac_address: str, device_name: str) -> bool:
    # * ------------------------------Pair and trust------------------------------
    print(f"‼️ Pairing to {device_name}")
    interactive_session = InteractiveSession()
    interactive_session.run_interactive(f"pair {device_mac_address}", wait=5)
    interactive_session.run_interactive(f"trust {device_mac_address}")
    print(f"✅ Paired")
    # * ------------------------------Pair and trust------------------------------

    print(f"‼️ Connecting to {device_mac_address}")
    deadline = time.time() + CONNECT_TIMEOUT
    while deadline > time.time():
        output = interactive_session.run(f"connect {device_mac_address}")
        if "Connection successful" in output or is_connected():
            return True

        print("⭕️Rertying...")
        time.sleep(2)

    return False
