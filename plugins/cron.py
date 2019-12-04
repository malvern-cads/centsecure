"""Removes All Cronjobs."""
import plugin
import common
import os
import shutil


class Cron(plugin.Plugin):
    """Removes All Cronjobs."""
    name = "Cron"
    os = ["Ubuntu"]
    os_version = ["14.04"]

    def execute(self):
        """Removes All Cronjobs."""
        path = "/var/spool/cron"
        common.backup(path, compress=True)

        # Definitely didn't copy this straight off Stack Overflow
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        common.info("Removed all cronjobs")
