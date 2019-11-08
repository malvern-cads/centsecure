"""A payload to configure the firewall."""

import payload
import common


class LinuxFirewall(payload.Payload):
    """Configure the firewall on Linux."""
    name = "Enable Linux Firewall"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        """Run the payload."""
        common.run("ufw enable")
