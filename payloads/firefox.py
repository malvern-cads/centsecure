import payload
import common
import os
import shutil

class Firefox(payload.Payload):
    name = "Firefox"
    os = ["All"]
    os_version = ["All"]

    def execute(self):
        common.warn("Make sure Firefox has been updated to the latest version (70+) in order for the settting to apply")
        self.add_user_js()

    def add_user_js(self):
        if "Windows" in payload.get_os():
            home_dir = "C:\\Users"
            profile_dir = "AppData\\Roaming\\Mozilla\\Firefox\\profiles"
        elif "Linux" in payload.get_os():
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
