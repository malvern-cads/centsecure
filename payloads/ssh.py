import payload
import common
import os


class SSH(payload.Payload):
    name = "SSH"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        path = "/etc/ssh/sshd_config"
        common.backup(path)

        # set correct permissions
        os.system("chown root:root {}".format(path))
        os.system("chmod og-rwx {}".format(path))

        # some fancy commands that ensure correct permissions on private keys
        os.system("find /etc/ssh -xdev -type f -name 'ssh_host_*_key' -exec chown root:root {} \\;")
        os.system("find /etc/ssh -xdev -type f -name 'ssh_host_*_key' -exec chmod 0600 {} \\;")

        # some fancy commands that ensure correct permissions on public keys
        os.system("find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub' -exec chmod 0644 {} \\;")
        os.system("find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub' -exec chown root:root {} \\;")

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
            "KeyAlgorithms": "curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group14-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256",
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
