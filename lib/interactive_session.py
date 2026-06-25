import subprocess


"""
Executes a single bluetoothctl command.

Args:
    cmd (str): The command to execute, excluding the "bluetoothctl" prefix.

Returns:
    str: The standard output (stdout) from the command, with leading and trailing whitespace removed.

Raises:
    subprocess.TimeoutExpired: If the command takes longer than 10 seconds to execute.
"""
def run(cmd: str) -> str:
    result = subprocess.run(
        ["bluetoothctl"] + cmd.split(),
        capture_output=True,
        text=True,
        timeout=10,
    )

    return result.stdout.strip()


"""
Executes a sequence of commands within a single, interactive bluetoothctl session.

Args:
    commands (list[str]): A list of strings, where each string represents a command to be executed in the interactive session.
    wait (float, optional): The timeout in seconds for the entire session. Defaults to 2.0.

Returns:
    str: The combined standard output (stdout) from all commands in the session, with leading and trailing whitespace removed.

Raises:
    subprocess.TimeoutExpired: If the interactive session takes longer than the specified wait time.
"""
def run_interactive(commands: list[str], wait: float = 2.0):
    input_str = "\n".join(commands) + "\n"
    result = subprocess.run(
        ["bluetoothctl"],
        input=input_str,
        capture_output=True,
        text=True,
        timeout=wait,
    )

    return result.stdout.strip()
