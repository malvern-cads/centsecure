"""A plugin for configuring SSH."""

import plugin
import common
import os


class Ssh(plugin.Plugin):
    """Configure SSH on Linux."""
    name = "SSH"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        """Execute plugin."""
        path = "/etc/ssh/sshd_config"
        if os.path.isfile(path):
            common.backup(path)
        else:
            common.info("{} not found, skipping SSH".format(path))
            return

        # set correct permissions
        common.run("chown root:root {}".format(path))
        common.run("chmod og-rwx {}".format(path))

        # some fancy commands that ensure correct permissions on private keys
        common.run_full("find /etc/ssh -xdev -type f -name 'ssh_host_*_key' -exec chown root:root {} \\;")
        common.run_full("find /etc/ssh -xdev -type f -name 'ssh_host_*_key' -exec chmod 0600 {} \\;")

        # some fancy commands that ensure correct permissions on public keys
        common.run_full("find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub' -exec chmod 0644 {} \\;")
        common.run_full("find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub' -exec chown root:root {} \\;")

        params = {
            "Protocol": "2",
            "LogLevel": "VERBOSE",
            "X11Forwarding": "no",
            "MaxAuthTries": "4",
            "IgnoreRhosts": "yes",
            "HostbasedAuthentication": "no",
            "PermitRootLogin": "no",
            "PermitEmptyPasswords": "no",
            "PermitUserEnvironment": "no",
            "Ciphers": "chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr",
            "MACs": "hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256",
            "KexAlgorithms": "curve25519-sha256@libssh.org,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256",
            "ClientAliveInterval": "300",
            "ClientAliveCountMax": "0",
            "LoginGraceTime": "60",
            "Banner": "/etc/issue.net",
            "UsePAM": "yes",
            "AllowTcpForwarding": "no",
            "maxstartups": "10:30:60",
            "MaxSessions": "4"
        }

        common.change_parameters(path, params)

        common.warn("Not doing anything about ssh access, (groups, users)")
