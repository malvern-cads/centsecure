"""Deals with Linux services."""
import plugin
import common


class LinuxServices(plugin.Plugin):
    """Deals with Linux services."""
    name = "Linux Services"
    os = ["Ubuntu"]
    os_version = ["14.04"]

    def execute(self):
        """Deals with Linux services."""
        services = self._get_services()

        good = ["acpid", "apparmor", "auditd", "console-setup", "dbus", "dns-clean", "grub-common", "irqbalance", "killprocs", "kmod", "lightdm", "networking", "ondemand", "open-vm-tools", "pppd-dns", "pulseaudio", "resolvconf", "rsyslog", "sendsigs", "sudo", "thermald", "udev", "umountfs", "umountnfs.sh", "umountroot", "unattended-upgrades", "urandom", "x11-common"]

        bad = ["anacron", "apport", "avahi-daemon", "bluetooth", "brltty", "cron", "cups", "cups-browsed", "friendly-recovery", "kerneloops", "rc.local", "rsync", "saned", "speech-dispatcher"]

        for service in services:
            if service in good:
                remove = False
            elif service in bad:
                remove = True
            else:
                remove = common.input_yesno("Do you want to removed the {} service".format(service))

            if remove:
                self._stop_service(service)
            else:
                self._enable_service(service)

    def _get_services(self):
        """Returns a list of available services.

        Return:
             list: services on the system

        """
        text = common.run("service --status-all", True)
        return [i[8:] for i in text.split("\n") if i != ""]

    def _stop_service(self, service):
        """Stops service.

            Args:
                service (str): The service to stop

        """
        common.debug("Stopping {} service".format(service))
        common.run("service {} stop".format(service))
        path = "/etc/init/{}.conf".format(service)
        try:
            self._comment_out(path)
        except FileNotFoundError:
            common.debug("Can't find {}".format(path))

    def _comment_out(self, path):
        """Comments out all of the lines in a file.

        Args:
            path (str): The path of the file

        """
        common.backup(path)
        with open(path) as in_file:
            lines = in_file.read().split("\n")

        new_lines = ["# " + line for line in lines]

        with open(path, "w") as out_file:
            out_file.write("\n".join(new_lines))

    def _enable_service(self, service):
        """Enable service.

        Args:
            service (str): The service to enable

        """
        pass
