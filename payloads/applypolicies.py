"""A payload to configure Windows policies."""

import payload
import common
import os
import win32net


class ApplyPolicies(payload.Payload):
    """Apply group and local policies to Windows."""
    name = "Apply Policies"
    os = ["Windows"]
    version = ["ALL"]

    def execute(self):
        """Execute the payload."""
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
