"""Secures Banners."""
import plugin
import common


class Banners(plugin.Plugin):
    """Secures Banners."""
    name = "Banner"
    os = ["Ubuntu"]
    os_version = ["14.04"]

    def execute(self):
        """Secures Banners."""
        self._write_file("/etc/motd", "CADS CyberCenturion\n")
        self._write_file("/etc/issue", "Authorized uses only. All activity may be monitored and reported.\n")
        self._write_file("/etc/issue.net", "Authorized uses only. All activity may be monitored and reported.\n")
        common.set_permissions("/etc/motd", "root", "root", "644")
        common.set_permissions("/etc/issue", "root", "root", "644")
        common.set_permissions("/etc/issue.net", "root", "root", "644")
        common.warn("Check if GDM is installed, and if so configure banners correctly")

    def _write_file(self, path, text):
        """Writes to a file.

        Args:
            path (str): the file to write to
            text (str): the text to be written

        """
        with open(path, "w+") as out_file:
            out_file.write(text)
