import sys

import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rich_print

from lib.check_state import is_powered
from lib.sys_interaction import (
    disconnect_device,
    get_connect_device_info,
    get_names_and_mac_addresses_of_devices,
    power_on,
    start_bluetoothctl_service,
    connect_device,
)
from lib.interactive_session import run


def start_connection():
    power_on()
    if not is_powered():
        is_started = start_bluetoothctl_service()
        if not is_started:
            print("❌ Failed to enable Bluetooth")
            sys.exit(1)

    print("✅ Bluetooth enabled")

    # ! Use { run } instead of { run_interactive }
    run("--timeout 5 scan on")

    result = ""
    while True:
        result = run("devices")
        if not result:
            run("--timeout 10 scan on")
        else:
            break

    devices_info = get_names_and_mac_addresses_of_devices(result)

    console = Console()
    table = Table(
        title="Available Devices", show_header=True, header_style="bold magenta"
    )

    table.add_column("MAC Address", style="cyan", justify="center")
    table.add_column("Device Name", style="cyan", justify="center")

    for mac_address, device_name in devices_info.items():
        table.add_row(mac_address, device_name)

    console.print(table)

    device_names = devices_info.values()
    choice = questionary.select("What's device connect?", choices=device_names).ask()

    mac_address = list(devices_info.keys())[list(device_names).index(choice)]
    device_name = devices_info[mac_address]

    if connect_device(mac_address, choice):
        print(f"✅ Connected to {device_name}")
    else:
        print("❌ Failed to connect...")


def start_desconnection():
    device_name, device_mac_address = get_connect_device_info().values()

    console = Console()
    console.print(
        Panel(
            f"[bold blue]{device_name}\n{device_mac_address}[/bold blue]",
            title="Connected device"
        )
    )

    answer = questionary.confirm("Do you really want to disconnect device?").ask()
    if not answer:
        sys.exit(0)

    if disconnect_device(device_mac_address):
        rich_print(f"[bold green]{device_name} was disconnected[/bold green]")
    else:
        rich_print(f"[bold red]Failed to disconnect {device_name}[/bold red]")


# * The main dict with primary functions
choice_actions = {
    "connect": start_connection,
    "disconnect": start_desconnection
}


# * THE PRIMARY FUNCTION
def start_session():
    choice = questionary.select(
        "What are we doing?..",
        choices=["Connect ear buds", "Disconnect ear buds", "Show saved devices"],
    ).ask()

    choice_actions[choice.lower().split()[0]]()
