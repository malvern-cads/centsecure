"""A payload to configure shadow."""

import common
import glob
import payload


class ShadowSuite(payload.Payload):
    """Configure shadowsuite."""
    name = "Secures Shadow Password Suite"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        """Execute payload."""
        self._set_password_config()
        self._check_shadow()
        self._set_shadow()
        self._set_profile()

    def _set_password_config(self):
        common.backup("/etc/shadow")
        path = "/etc/login.defs"
        common.backup(path)

        params = {
            "PASS_MAX_DAYS": "365",
            "PASS_MIN_DAYS": "7",
            "PASS_WARN_AGE": "7"
        }

        common.change_parameters(path, params)

        # inactive password lock
        common.run("useradd -D -f 30")

        users = common.get_current_users()
        for user in users:
            common.run_full("chage --lastday $(date +%Y/%m/%d) {}".format(user))
            common.run("chage --maxdays 365 {}".format(user))
            common.run("chage --mindays 7 {}".format(user))
            common.run("chage --warndays 7 {}".format(user))
            common.run("chage --inactive 30 {}".format(user))

    def _check_shadow(self):
        # check passwords have been changed in the pass
        # TODO do this automatically
        cmd = "for usr in $(cut -d: -f1 /etc/shadow); do [[ $(chage --list $usr | grep '^Last password change' | cut -d: -f2) > $(date) ]] && echo \"$usr :$(chage --list $usr | grep '^Last password change' | cut -d: -f2)\"; done"
        output = common.run_full(cmd)
        if output != "":
            common.info("Ensure these are all in the past:\n" + str(output))

    def _set_shadow(self):
        # sets all system accounts to a no log on shell
        common.run_full("awk -F: '($1!=\"root\" && $1!=\"sync\" && $1!=\"shutdown\" && $1!=\"halt\" && $1!~/^\\+/ && $3<'\"$(awk '/^\\s*UID_MIN/{print $2}' /etc/login.defs)\"' && $7!=\"'\"$(which nologin)\"'\" && $7!=\"/bin/false\") {print $1}' /etc/passwd | while read user; do usermod -s $(which nologin) $user; done")

        # locks all non root system accounts
        common.run_full("awk -F: '($1!=\"root\" && $1!~/^\\+/ && $3<'\"$(awk '/^\\s*UID_MIN/{print $2}' /etc/login.defs)\"') {print $1}' /etc/passwd | xargs -I '{}' passwd -S '{}' | awk '($2!=\"L\" && $2!=\"LK\") {print $1}' | while read user; do usermod -L $user; done")

        # sets root group uid to 0
        common.run("usermod -g 0 root")

    def _set_profile(self):
        # set umask and shell timeout
        profiles = ["/etc/bashrc", "/etc/bash.bashrc", "/etc/profile"]
        for profile in profiles:
            try:
                common.backup(profile)
                with open(profile, "a") as out_file:
                    out_file.write("\numask 027\nTMOUT=900\n")
            except FileNotFoundError:
                continue

        # sets umask
        alt_profiles = glob.glob("/etc/profile.d/*.sh")
        for profile in alt_profiles:
            common.backup(profile)
            with open(profile, "a") as out_file:
                out_file.write("\numask 027\n")

    # something to manually check: cat /etc/securetty TODO

    # /etc/pam.d/sufile:auth required pam_wheel.so use_uid TODO
    # wheel:x:10:root,<user list>
