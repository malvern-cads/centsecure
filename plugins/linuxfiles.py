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
        self._set_permissions("/etc/passwd", "root", "root", "644")
        self._set_permissions("/etc/shadow", "root", "shadow", "o-rwx,g-wx")
        self._set_permissions("/etc/group", "root", "root", "644")
        self._set_permissions("/etc/gshadow", "root", "shadow", "o-rwx,g-rw")
        self._set_permissions("/etc/passwd-", "root", "root", "u-x,go-wx")
        self._set_permissions("/etc/shadow-", "root", "root", "o-rwx,g-rw")
        self._set_permissions("/etc/group-", "root", "root", "u-x,go-wx")
        self._set_permissions("/etc/gshadow-", "root", "root", "o-rwx,g-rw")

        common.warn("Check there are no rough programs:")
        common.stdout(common.run_full("df --local -P | awk {'if (NR!=1) print $6'} | xargs -I '{}' find '{}' -xdev -type f -perm -4000"))

    def _set_permissions(self, path, user, group, permissions):
        """Sets permissions on file.

        Args:
            path (str): path of file
            user (str): owner of file
            group (str): group owner of file
            permissions (str): permissions to be set on file

        """
        common.backup(path)
        common.run_full("chown {}:{} {}".format(user, group, path))
        common.run_full("chmod {} {}".format(permissions, path))
