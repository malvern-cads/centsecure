import payload
import common
import os


class ApplyPolicies(payload.Payload):
    name = "Apply Policies"
    os = ["Windows"]
    version = ["ALL"]

    def execute(self):
        common.info("Applying Local Security Policy...")
        cmd = "secedit.exe /configure /db %windir%\\security\\local.sdb /cfg policies\\security_policy.inf"
        os.system(cmd)

        # displays access is denies but still runs
        common.info("Applying Firewall Policy...")
        cmd = "netsh advfirewall import \"policies\\firewall.wfw\""
        os.system(cmd)

        # TODO doesn't appear in gui but does from cmd??
        common.info("Applying Advanced Audit Policies...")
        cmd = "auditpol /restore /file:policies\\audit.csv"
        os.system(cmd)
