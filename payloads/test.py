import payload


class Windows10Firewall(payload.Payload):
    name = "Windows 10 Firewall"
    os = "Windows"
    os_version = "10"

    def __init__(self):
        print("Windows10Firewall instance created!")

    def execute(self):
        print("Windows10Firewall has been executed!")


class LinuxFirewall(payload.Payload):
    name = "Linux Firewall"
    os = "Linux"
    os_version = ["9", "10"]

    def __init__(self):
        print("LinuxFirewall instance created!")

    def execute(self):
        print("LinuxFirewall has been executed!")
