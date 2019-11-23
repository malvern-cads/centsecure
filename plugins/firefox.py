import plugin
import common
import os
import shutil


class Firefox(plugin.Plugin):
    """Configure Firefox using user.js on all operating systems."""
    name = "Firefox"
    os = ["All"]
    os_version = ["All"]

    def execute(self):
        """Execute plugin."""
        reminder = "Make sure Firefox has been updated to the latest version (70+) in order for the settting to apply\nFirefox will have to be restarted"
        common.reminder(reminder)
        self._add_user_js()

    def _add_user_js(self):
        if "Windows" in plugin.get_os():
            home_dir = "C:\\Users"
            profile_dir = "AppData\\Roaming\\Mozilla\\Firefox\\profiles"
        elif "Linux" in plugin.get_os():
            home_dir = "/home/"
            profile_dir = ".mozilla/firefox/"

        home_dirs = os.listdir(home_dir)

        for home in home_dirs:
            current_profile_dir = os.path.join(home_dir, home, profile_dir)

            if os.path.isdir(current_profile_dir):
                common.info("Adding user.js for {}".format(home))
                profiles = os.listdir(current_profile_dir)

                for profile in profiles:
                    path = os.path.join(current_profile_dir, profile)
                    if os.path.isdir(path):
                        shutil.copy("user.js", path)
