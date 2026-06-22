import subprocess
import getpass
import sys


def run(cmd: str) -> str:
    result = subprocess.run(
        ["bluetoothctl"] + cmd.split(), capture_output=True, text=True, timeout=10
    )

    return result.stdout.strip()


def run_interactive(commands: list[str], wait: float = 2.0):
    input_str = "\n".join(commands) + "\n"
    result = subprocess.run(
        ["bluetoothctl"], input=input_str, capture_output=True, text=True, timeout=wait
    )

    return result.stdout.strip()


def start_bluetoothctl_service() -> bool:
    unblock_hardware_result = subprocess.run(
        ["rfkill", "unblock", "bluetooth"], capture_output=True  #
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
