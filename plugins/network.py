"""Secures Network."""
import plugin
import common


class Network(plugin.Plugin):
    """Secures Network."""
    name = "Network"
    os = ["Ubuntu"]
    os_version = ["14.04"]

    def execute(self):
        """Secures Network."""
        common.warn("Assuming this is a host machine")

        self._secure_ipv4()
        self._secure_ipv6()
        self._enable_tcp_wrappers()
        self._configure_hosts()
        self._secure_protocols()
        self._secure_firewall()
        self._remove_interfaces()

    def _secure_ipv4(self):
        """Secures IPV4."""
        # Kernel Parameters
        params = {
            "net.ipv4.ip_forward": "0",
            "net.ipv4.conf.all.send_redirects": "0",
            "net.ipv4.conf.default.send_redirects": "0",
            "net.ipv4.conf.all.accept_source_route": "0",
            "net.ipv4.conf.default.accept_source_route": "0",
            "net.ipv4.conf.all.accept_redirects": "0",
            "net.ipv4.conf.default.accept_redirects": "0",
            "net.ipv4.conf.all.secure_redirects": "0",
            "net.ipv4.conf.default.secure_redirects": "0",
            "net.ipv4.conf.all.log_martians": "1",
            "net.ipv4.conf.default.log_martians": "1",
            "net.ipv4.icmp_echo_ignore_broadcasts": "1",
            "net.ipv4.icmp_ignore_bogus_error_responses": "1",
            "net.ipv4.conf.all.rp_filter": "1",
            "net.ipv4.conf.default.rp_filter": "1",
            "net.ipv4.tcp_syncookies": "1"
        }
        common.change_parameters("/etc/sysctl.conf", params, True)

        # Current kernel parameters
        common.run("sysctl -w net.ipv4.ip_forward=0")
        common.run("sysctl -w net.ipv4.conf.all.send_redirects=0")
        common.run("sysctl -w net.ipv4.conf.default.send_redirects=0")
        common.run("sysctl -w net.ipv4.conf.all.accept_source_route=0")
        common.run("sysctl -w net.ipv4.conf.default.accept_source_route=0")
        common.run("sysctl -w net.ipv4.conf.all.accept_redirects=0")
        common.run("sysctl -w net.ipv4.conf.default.accept_redirects=0")
        common.run("sysctl -w net.ipv4.conf.all.secure_redirects=0")
        common.run("sysctl -w net.ipv4.conf.default.secure_redirects=0")
        common.run("sysctl -w net.ipv4.conf.all.log_martians=1")
        common.run("sysctl -w net.ipv4.conf.default.log_martians=1")
        common.run("sysctl -w net.ipv4.icmp_echo_ignore_broadcasts=1")
        common.run("sysctl -w net.ipv4.icmp_ignore_bogus_error_responses=1")
        common.run("sysctl -w net.ipv4.conf.all.rp_filter=1")
        common.run("sysctl -w net.ipv4.conf.default.rp_filter=1")
        common.run("sysctl -w net.ipv4.tcp_syncookies=1")
        common.run("sysctl -w net.ipv4.route.flush=1")

    def _secure_ipv6(self):
        """Secures IPV6."""
        # Kernel parameters
        params = {
            "net.ipv6.conf.all.accept_ra": "0",
            "net.ipv6.conf.default.accept_ra": "0",
            "net.ipv6.conf.all.accept_redirects": "0",
            "net.ipv6.conf.default.accept_redirects": "0"
        }
        common.change_parameters("/etc/sysctl.conf", params, True)

        # Current kernel parameters
        common.run("sysctl -w net.ipv6.conf.all.accept_ra=0")
        common.run("sysctl -w net.ipv6.conf.default.accept_ra=0")
        common.run("sysctl -w net.ipv6.conf.all.accept_redirects=0")
        common.run("sysctl -w net.ipv6.conf.default.accept_redirects=0")
        common.run("sysctl -w net.ipv6.route.flush=1")

    def _enable_tcp_wrappers(self):
        """Installs TCPD."""
        common.run("apt install tcpd")

    def _configure_hosts(self):
        """Secure allow and deny hosts files."""
        common.backup("/etc/hosts.allow")
        common.backup("/etc/hosts.deny")

        common.warn("You need to set up /etc/hosts.allow")
        common.warn("In the format: 'ALL: <net>/<mask>, <net>/<mask>'")

        with open("/etc/hosts.deny", "w") as out_file:
            out_file.write("ALL: ALL")

        common.set_permissions("/etc/hosts.allow", "root", "root", "644")
        common.set_permissions("/etc/hosts.deny", "root", "root", "644")

    def _secure_protocols(self):
        """Ensures protocols are disabled."""
        text = "install dccp /bin/true\ninstall sctp /bin/true\ninstall rds /bin/true\ninstall tipc /bin/true\n"
        with open("/etc/modprobe.d/CIS.conf", "w") as out_file:
            out_file.write(text)

    def _secure_firewall(self):
        """Ensures the firewall is secured."""
        path = "policies/firewall.sh"
        common.set_permissions(path, "root", "root", "744")
        common.run(path)

    def _remove_interfaces(self):
        """Remove Wireless Interfaces."""
        common.warn("Please disable any wifi interfaces")
        common.warn("ip link set <interface> down")
        common.stdout(common.run("iwconfig"))
