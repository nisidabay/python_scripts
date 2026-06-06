#!/usr/bin/python3
# type: ignore
# Stops a process by name
################################################################################
import time
import click
import psutil
from typing import Optional


@click.command()
@click.option("-name", type=str, required=True, help="Name of the process to stop")
@click.option(
    "-delay",
    type=int,
    default=1,
    show_default=True,
    help="Time in minutes to stop",
)
def run(name: str, delay: int) -> None:
    """Stop a process"""
    pid = get_pid(name)
    if pid:
        click.echo(f"Found process: <{name}> with id: {pid}")
    scheduled_time(delay, pid, name)


def get_pid(name: str) -> Optional[int]:  # sourcery skip: use-next
    """Get process id"""

    for process in psutil.process_iter(attrs=["pid", "name"]):
        if name in process.info["name"]:
            return process.info["pid"]
    return None


def stop_process(pid: int) -> None:
    """Stop the process"""

    if pid is not None:
        try:
            process = psutil.Process(pid)
            process.terminate()
            click.echo(f"Process with PID {pid} terminated.")
        except psutil.NoSuchProcess:
            click.echo(f"Process with PID {pid} not found.")
    else:
        click.echo("Process not found.")


def scheduled_time(delay: float, pid: int, name=str):
    """Schedule the process to be stopped after a certain time"""

    scheduled_time = time.time() + (delay * 60)  # Convert to seconds
    click.echo(f"Process <{name}> scheduled for killing")
    while time.time() < scheduled_time:
        time.sleep(1)
    stop_process(pid)


if __name__ == "__main__":
    run()
