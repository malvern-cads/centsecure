"""A plugin to configure LightDM."""

import plugin
import configparser
import common


class Lightdm(plugin.Plugin):
    """Configure LightDM."""
    name = "Lightdm securing"
    os = ["Ubuntu"]
    os_version = ["16.04"]

    def execute(self):
        """Execute plugin."""
        path = "/etc/lightdm/lightdm.conf"
        config = configparser.ConfigParser()
        try:
            common.backup(path)
            config.read(path)
        except FileNotFoundError as ex:
            common.error("{} not found".format(path), ex)

        config["Seat:*"] = {}
        config["Seat:*"]["user-session"] = "ubuntu"
        config["Seat:*"]["greeter-session"] = "unity-greeter"
        config["Seat:*"]["greeter-show-manual-login"] = "true"
        config["Seat:*"]["greeter-hide-users"] = "true"
        config["Seat:*"]["allow-guest"] = "false"

        with open(path, "w+") as out_file:
            config.write(out_file)

        common.info("{} updated".format(path))
