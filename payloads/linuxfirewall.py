import payload
import os
import common


class LinuxFirewall(payload.Payload):
    name = "Enable Linux Firewall"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        common.debug("Linux Firewall is being executed")
        os.system("ufw enable")
        common.debug("Linux Firewall has finished")
