import plugin
import common
import os
import shutil


class LinuxAudit(plugin.Plugin):
    """Enables auditing for Linux."""
    name = "Linux Audit"
    os = ["Ubuntu"]
    os_version = ["14.04"]

    def execute(self):
        """Enables auditing for Linux."""
        self._enable_auditd()
        self._apply_audit_conf()
        self._update_grub()
        self._apply_audit_rules()

    def _enable_auditd(self):
        """Enables auditd."""
        common.run("apt install auditd -y")
        common.run("update-rc.d auditd enable")

    def _apply_audit_conf(self):
        """Applies custom auditd.conf."""
        common.debug("Applying auditd conf")
        path = "/etc/audit/auditd.conf"
        common.backup(path)
        os.remove(path)
        shutil.copy2("policies/auditd.conf", path)

    def _update_grub(self):
        """Updates grub so auditd can audit pre init."""
        # TODO
        # GRUB_CMDLINE_LINUX="audit=1" needs to be added to /etc/default/grub
        # then update-grub
        pass

    def _apply_audit_rules(self):
        """Applies custom audit.rules."""
        common.debug("Applying audit rules")
        paths = ["/etc/audit/audit.rules", "/etc/audit/rules.d/audit.rules"]

        for path in paths:
            common.backup(path)
            os.remove(path)

            if common.is_os_64bit():
                source = "policies/audit.rules.64"
            else:
                source = "policies/audit.rules.32"

            shutil.copy2(source, path)
            
            output = common.run_full("find /dev/sda1 -xdev \\( -perm -4000 -o -perm -2000 \\) -type f | awk '{print \"-a always,exit -F path=\" $1 \" -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged\" }'")

            if output:
                with open(path, "a") as out_file:
                    out_file.write("\n{}\n".format(output))

            # Lock Rules
            common.run("auditctl -e 2")
