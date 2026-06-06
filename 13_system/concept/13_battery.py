#!/usr/bin/python3
#
# Check battery percentage and send notification."""

import psutil
from notifypy import Notify


def check_battery() -> None:
    """Check battery percentage and send notification."""

    battery = psutil.sensors_battery()
    percent = battery.percent

    if battery.power_plugged:
        message = f"Charging - {percent:.2f}% Battery"
    else:
        message = f"{percent:.2f}% Battery remaining"

    send_notification("Battery Info", message)


def send_notification(title: str, message: str) -> None:
    """Send a desktop notification.

    Args:
        title: Notification title
        message: Notification message
    """

    notification = Notify()
    notification.title = title
    notification.message = message
    notification.send()


if __name__ == "__main__":
    check_battery()
