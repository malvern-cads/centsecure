import payload
import os


class LinuxFirewall(payload.Payload):
    name = "Enable Linux Firewall"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        os.system("ufw enable")
