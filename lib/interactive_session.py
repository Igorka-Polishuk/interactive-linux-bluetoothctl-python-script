import subprocess


class InteractiveSession:
    def __init__(self):
        self.__main_command_line_util = "bluetoothctl"

    def run(self, cmd: str) -> str:
        result = subprocess.run(
            [self.__main_command_line_util] + cmd.split(),
            capture_output=True,
            text=True,
            timeout=10,
        )

        return result.stdout.strip()

    def run_interactive(self, commands: list[str], wait: float = 2.0):
        input_str = "\n".join(commands) + "\n"
        result = subprocess.run(
            [self.__main_command_line_util],
            input=input_str,
            capture_output=True,
            text=True,
            timeout=wait,
        )

        return result.stdout.strip()
