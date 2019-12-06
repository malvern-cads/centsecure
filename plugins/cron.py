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
        self._remove_user_jobs()
        self._remove_system_jobs()

    def _remove_user_jobs(self):
        """Removes all user cronjobs."""
        path = "/var/spool/cron"
        common.backup(path, compress=True)

        # Definitely didn't copy this straight off Stack Overflow
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        common.debug("Removed all user cronjobs")

    def _remove_system_jobs(self):
        """Removes all system cronjobs."""
        targets = ["/etc/anacrontab", "/etc/crontab", "/etc/cron.d", "/etc/cron.daily", "/etc/cron.hourly", "/etc/cron.monthly", "/etc/cron.weekly", "/var/spool/anacron"]
        for target in targets:
            self._remove_and_backup(target)

    def _remove_and_backup(self, path):
        """Backs up file and removes it.

        Args:
            path (str): the path to remove

        """
        if os.path.isfile(path):
            common.backup(path, compress=True)
            os.remove(path)  # remove the file
        elif os.path.isdir(path):
            common.backup(path, compress=True)
            shutil.rmtree(path)  # remove dir and all contains
