import payload
import configparser
import common


class Lightdm(payload.Payload):
    name = "Lightdm securing"
    os = ["Ubuntu"]
    os_version = ["16.04"]

    def execute(self):
        print("Lightdm has been executed!")
        path = "/etc/lightdm/lightdm.conf"
        config = configparser.ConfigParser()
        try:
            common.backup(path)
            config.read(path)
        except FileNotFoundError:
            print("{} not found".format(path))
        config["SeatDefaults"] = {}
        config["SeatDefaults"]["user-session"] = "ubuntu"
        config["SeatDefaults"]["greeter-session"] = "unity-greeter"
        config["SeatDefaults"]["greeter-show-manual-login"] = "true"
        config["SeatDefaults"]["greeter-hide-users"] = "true"
        config["SeatDefaults"]["allow-guest"] = "false"

        with open(path, "w+") as out_file:
            config.write(out_file)
        print("{} updated".format(path))
        print("Lightdm has finished")
