"""Sets Permissions on Important Files."""
import plugin
import common


class LinuxFiles(plugin.Plugin):
    """Sets Permissions on Important Files."""
    name = "Secure Core Files"
    os = ["Ubuntu"]
    os_version = ["14.04"]

    def execute(self):
        """Sets Permissions on Important Files."""
        common.set_permissions("/etc/passwd", "root", "root", "644")
        common.set_permissions("/etc/shadow", "root", "shadow", "o-rwx,g-wx")
        common.set_permissions("/etc/group", "root", "root", "644")
        common.set_permissions("/etc/gshadow", "root", "shadow", "o-rwx,g-rw")
        common.set_permissions("/etc/passwd-", "root", "root", "u-x,go-wx")
        common.set_permissions("/etc/shadow-", "root", "root", "o-rwx,g-rw")
        common.set_permissions("/etc/group-", "root", "root", "u-x,go-wx")
        common.set_permissions("/etc/gshadow-", "root", "root", "o-rwx,g-rw")

        reminder = "Check there are no rouge programs:\n" + common.run_full("df --local -P | awk {'if (NR!=1) print $6'} | xargs -I '{}' find '{}' -xdev -type f -perm -4000")
        common.reminder(reminder)
