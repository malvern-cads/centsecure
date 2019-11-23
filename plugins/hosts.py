"""Secures hosts file."""
import plugin
import common


class Hosts(plugin.Plugin):
    """Secures hosts file."""
    name = "Hosts"
    os = ["All"]
    os_version = ["All"]

    def execute(self):
        """Secures hosts file."""
        self._set_default_hosts()

    def _set_default_hosts(self):
        """Clears hosts and sets default hostname."""
        if "Linux" in plugin.get_os():
            hostname = "CADSHOST"

            common.backup("/etc/hostname")
            with open("/etc/hostname", "w") as out_file:
                out_file.write(hostname + "\n")

            with open("policies/hosts") as in_file:
                text = in_file.read()
            hosts = text.format(hostname)

            common.backup("/etc/hosts")
            with open("/etc/hosts", "w") as out_file:
                out_file.write(hosts)

            common.run("hostname {}".format(hostname))
        else:
            with open("policies/hosts.win") as in_file:
                text = in_file.read()
            path = "C:\\Windows\\System32\\drivers\\etc\\hosts"
            # common.backup(path)
            with open(path, "w") as out_file:
                out_file.write(text)
