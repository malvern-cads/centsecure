"""A payload to manage updates."""

import payload
import common


class DebianUpdate(payload.Payload):
    """Run Debian Updates."""
    name = "Debian Updates"
    os = ["Ubuntu"]
    os_version = ["all"]
    priority = 11

    def execute(self):
        """Run the payload."""
        # Update system package lists
        common.run("apt-get update")
        # Update available packages
        common.run("apt-get upgrade -y")


class WindowsUpdates(payload.Payload):
    """Download updates for Windows."""
    name = "Download Windows Updates"
    os = ["Windows"]
    os_version = ["all"]
    priority = 3  # High priority, it can download while we are doing other stuff

    def execute(self):
        """Run the payload."""
        # NOTE: This command does not block (i.e. it won't wait until it has finished)
        common.run("wuauclt.exe /updatenow")
