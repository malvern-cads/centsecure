import payload
import common


class LinuxFirewall(payload.Payload):
    name = "Enable Linux Firewall"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        common.run("ufw enable")
