"""A plugin to configure Windows policies."""

import plugin
import common
import os
import win32net


class ApplyPolicies(plugin.Plugin):
    """Apply group and local policies to Windows."""
    name = "Apply Policies"
    os = ["Windows"]
    version = ["ALL"]

    def execute(self):
        """Execute the plugin."""
        common.info("Applying Local Security Policy...")
        cmd = "secedit.exe /configure /db %windir%\\security\\local.sdb /cfg policies\\security_policy.inf"
        os.system(cmd)

        # displays access is denies but still runs
        common.info("Applying Firewall Policy...")
        cmd = "netsh advfirewall import \"policies\\firewall.wfw\""
        os.system(cmd)

        # TODO doesn't appear in gui but does from cmd??
        # No idea if this actually works...
        common.info("Applying Advanced Audit Policies...")
        cmd = "auditpol /restore /file:policies\\audit.csv"
        os.system(cmd)

        # Removes all shares
        common.info("Removing all shares")
        for share in win32net.NetShareEnum(None, 0)[0]:
            win32net.NetShareDel(None, share['netname'])

        # Disables Default Services
        common.info("Disabling Services...")
        common.import_reg("policies\\services.reg")

        # Apply the master registry file
        # This contains lots of useful registry keys that aren't big enough to group on their own
        common.info("Applying Master Registry...")
        common.import_reg("policies\\master.reg")

        self._disableFeatures()


    def _disableFeatures(self):
        """Disables All Windows Features.

        Also renables IE.

        """
        common.info("Disabling Windows Features")
        # Gets all currently enabled features
        output = common.run_full('DISM /online /get-features /format:table | find "Enabled"')
        bad = [feature.split()[0] for feature in output.split("\n") if feature != ""]
        common.debug("Found features: {}".format(bad))
        for feature in bad:
            common.debug("Disabling {}...".format(feature))
            common.run_full("DISM /online /disable-feature /featurename:{} /NoRestart".format(feature))

        if common.is_os_64bit():
            ie = "Internet-Explorer-Optional-amd64"
        else:
            ie = "Internet-Explorer-Optional-x86"
        common.info("Enabling IE")
        common.run_full("DISM /online /enable-feature /featurename:{} /NoRestart".format(ie))
