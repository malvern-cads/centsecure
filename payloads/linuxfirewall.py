import payload
import os

class LinuxFirewall(payload.Payload):
    name = "Enable Linux Firewall"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        print("Linux Firewall is being executed")
        os.system("ufw enable")
        print("Linux Firewall has finished")
