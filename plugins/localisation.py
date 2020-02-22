"""Set language and keyboard preferences on the machine."""
import plugin
import common


class Localisation(plugin.Plugin):
    """Set language and keyboard preferences on the machine."""
    name = "Localisation"
    os = ["All"]
    os_version = ["All"]
    priority = -1  # Negative priority will be run first

    def execute(self):
        """Execute the payload."""
        if "Windows" in plugin.get_os():
            self._windows()
        else:
            common.debug("Skipping localisation")

    def _windows(self):
        # Set the keyboard layout to en-GB
        common.run(["powershell.exe", "Set-WinUserLanguageList -Force en-GB"])
