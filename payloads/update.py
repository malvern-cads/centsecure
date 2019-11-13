"""A payload to manage updates."""

import payload
import common

# /etc/apt/apt.conf.d/50-unattended-upgrades
UNATTENDED_UPGRADE_CONFIG = """
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESM:${distro_codename}";
    "${distro_id}ESM:${distro_codename}-security";
};

Unattended-Upgrade::Package-Blacklist {

};

Unattended-Upgrade::DevRelease "auto";
"""

# /etc/apt/apt.conf.d/20-auto-upgrades
AUTO_UPGRADE_CONFIG = """
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
"""


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


class UbuntuAutomaticUpdates(payload.Payload):
    """Setup automatic updates for Ubuntu."""
    name = "Ubuntu Automatic Updates"
    os = ["Ubuntu"]
    os_version = ["all"]

    def execute(self):
        """Run the payload."""
        common.run("apt-get install unattended-upgrades -y")
        common.debug("Writing unattended upgrade configuration files...")
        common.write_file("/etc/apt/apt.conf.d/50-unattended-upgrades", UNATTENDED_UPGRADE_CONFIG)
        common.write_file("/etc/apt/apt.conf.d/20-auto-upgrades", AUTO_UPGRADE_CONFIG)


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
