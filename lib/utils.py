from rich import print as rich_print


# * |------------------------------Print Utils------------------------------/
def print_successful_msg(msg: str):
    rich_print(f"[bold green]{msg}[/bold green]")


def print_failed_msg(msg: str):
    rich_print(f"[bold red]{msg}[/bold red]")


def print_processing_msg(msg: str):
    rich_print(f"[italic blue]{msg}[/italic blue]")

def print_retrying_msg(msg: str):
    rich_print(f"[underline yellow]{msg}[/underline yellow]")
# * /------------------------------Print Utils------------------------------|
