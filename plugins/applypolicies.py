"""A plugin to configure Windows policies."""

import plugin
import common
import os
import win32net
import subprocess


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
        try:
            for share in win32net.NetShareEnum(None, 0)[0]:
                win32net.NetShareDel(None, share['netname'])
        except Exception as e:
            common.warn("Not running remove shares")
            common.debug(e)

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
        if common.is_os_64bit():
            dism = "%WINDIR%\\SysNative\\dism.exe"
            ie = "Internet-Explorer-Optional-amd64"
        else:
            dism = "DISM"
            ie = "Internet-Explorer-Optional-x86"

        # Gets all currently enabled features
        output = common.run_full('{} /online /get-features /format:table | find "Enabled"'.format(dism))
        bad_features = [feature.split()[0] for feature in output.split("\n") if feature != ""]
        common.debug("Found features: {}".format(bad_features))

        outputs = []
        for feature in bad_features:
            # Causes BSOD if you disable these
            if feature in ["Printing-Foundation-Features", "FaxServicesClientPackage"]:
                common.debug("Keeping {}...".format(feature))
                continue
            common.debug("Disabling {}...".format(feature))
            process = self._run_background("{} /online /disable-feature /featurename:{} /NoRestart".format(dism, feature))
            outputs.append([feature, process])

        common.info("Enabling IE")
        process = self._run_background("{} /online /enable-feature /featurename:{} /NoRestart".format(dism, ie))
        outputs.append(["IE", process])

        # Currently we do not check for outputs

    def _run_background(self, cmd):
        """Runs shell command in background.

        Args:
            cmd (str): the command to be run

        Returns:
            something: the subprocess
        """
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return process
