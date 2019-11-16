import plugin
import common


class LinuxServices(plugin.Plugin):
    name = "Linux Services"
    os = ["Ubuntu"]
    os_version = ["14.04"]

    def execute(self):
        services = self.get_services()

        for service in services:
            yes = common.input_yesno("Do you want to removed the {} service".format(service))
            if yes:
                self.stop_service(service)

    def get_services(self):
        text = common.run("service --status-all", True)
        return [i[8:] for i in text.split("\n") if i != ""]

    def stop_service(self, service):
        common.debug("Stopping {} service".format(service))
        common.run("service {} stop".format(service))
