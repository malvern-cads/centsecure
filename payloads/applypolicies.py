import payload
import common


class ApplyPolicies(payload.Payload):
    name = "Apply Policies"
    os = ["Windows"]
    version = ["ALL"]

    def execute(self):
        common.info("Applying Local Security Policy...")
        cmd = "secedit.exe /configure /db %windir%\\security\\local.sdb /cfg policies\\security_policy.inf"
        common.stdout(common.run(cmd))

        # displays access is denies but still runs
        common.info("Applying Firewall Policy...")
        cmd = "netsh advfirewall import \"policies\\firewall.wfw\""
        common.stdout(common.run(cmd))

        # TODO doesn't appear in gui but does from cmd??
        # No idea if this actually works...
        common.info("Applying Advanced Audit Policies...")
        cmd = "auditpol /restore /file:policies\\audit.csv"
        common.stdout(common.run(cmd))
