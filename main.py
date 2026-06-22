import sys
import time

from utils.constants import CONNECT_TIMEOUT, DEVICE_MAC, DEVICE_NAME
from utils.check_state import is_connected, is_paired, is_powered
from lib.sys_interact import run, run_interactive, start_bluetoothctl_service


def power_on():
    print("Enabling Bluetooth...")
    run("power on")
    time.sleep(1)


def pair_device():
    print(f"Pairing with {DEVICE_NAME}")
    run_interactive(["--timeout 15 scan on"], wait=5)
    run_interactive(["scan off"])
    run_interactive(f"pair {DEVICE_MAC}", wait=5)
    run_interactive(f"trust {DEVICE_MAC}")


def connect_device() -> bool:
    print(f"Connecting to {DEVICE_NAME}")
    deadline = time.time() + CONNECT_TIMEOUT
    while deadline > time.time():
        output = run_interactive([f"connect {DEVICE_MAC}"], wait=5)
        if "Connection successful" in output or is_connected():
            print(f"✅ Connected to {DEVICE_NAME}")
            return True

        print("Rertying...")
        time.sleep(2)

    return False


# * 1. Power on bluetooth
# * 2. If bluetooth is not powered on -> start bluetooth service by hitting sudo password { start_bluetoothctl_service }
# * 3. If headphones are not paired -> pair them { pair_device }
# * 4. Try to connect to headphones { connect_device }, if everything is okay -> alert user, else -> alert user about shit and kill script
def main():
    power_on()
    if not is_powered():
        is_started = start_bluetoothctl_service()
        if not is_started:
            print("❌ Failed to enable Bluetooth")
            sys.exit(1)

    print("✅ Bluetooth enabled")

    if not is_paired():
        pair_device()

    print("✅ Device paired")

    if connect_device():
        print("✅ Device connected")
    else:
        print("❌ Device didn't connect")
        sys.exit(1)


if __name__ == "__main__":
    main()
