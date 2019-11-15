"""A plugin to configure the firewall."""

import plugin
import common


class LinuxFirewall(plugin.Plugin):
    """Configure the firewall on Linux."""
    name = "Enable Linux Firewall"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        """Run the plugin."""
        common.run("ufw enable")
