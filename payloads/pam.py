import payload
import shutil
import os
import common


# list all pam modules available: sudo updatedb && locate --regex '.*/pam_[^/]+\.so$'
class Pam(payload.Payload):
    name = "Secure PAM"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        self.set_password_requirements()
        self.set_password_lockout()

    def set_password_requirements(self):  # also deals with password reuse and ensuring sha512 is used
        # /etc/pam.d/system-auth - check if exists due to alternative method of implementation
        path = "/etc/pam.d/system-auth"
        if os.path.isfile(path):
            common.warn("{} exists, needs checking (cracklib/pwquality)".format(path))

        path = "/etc/pam.d/common-password"
        common.backup(path)
        # we need to ensure cracklib is installed, it will also change common-password
        os.system("sudo apt install libpam-cracklib -y -q")
        common.backup(path)

        with open(path) as in_file:
            lines = in_file.read().split("\n")

        cracklib_index = None
        pwquality_index = None
        unix_index = None

        for index, line in enumerate(lines):
            if "pam_cracklib.so" in line:
                cracklib_index = index
            elif "pam_pwquality.so" in line:
                pwquality_index = index
            elif "pam_unix.so" in line:
                unix_index = index

        cracklib = "password required pam_cracklib.so try_first_pass retry=3 minlen=14 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1"
        pwquality = "password requisite pam_pwquality.so try_first_pass retry=3"

        # we can also ensure that it remembers passwords
        unix = "password sufficient pam_unix.so sha512 shadow use_authtok remember=5"

        if unix_index is not None:
            lines[unix_index] = unix
        else:
            common.error("Error, could not find unix_index, {} is misconfigured".format(path))
            return

        # You can use either cracklib or pwquality, but one of them must be used
        if cracklib_index is not None:
            lines[cracklib_index] = cracklib
        elif pwquality_index is not None:
            common.debug("pwquality is used instead of cracklib")
            lines[pwquality_index] = pwquality
        else:  # no cracklib or pwquality, we'll add cracklib (in the right place)
            common.error("Cracklib is not configured correctly")
            return

        with open(path, "w") as out_file:
            out_file.write("\n".join(lines))

        # This only needs to be done for the pwquality, although it can't hurt to do it anyway
        path = "/etc/security/pwquality.conf"
        common.backup(path)
        with open(path, "w") as out_file:
            text = "minlen = 14\ndcredit = -1\nucredit = -1\nocredit = -1\nlcredit = -1"
            out_file.write(text)

        common.info("Added Password requirements")

    def set_password_lockout(self):
        paths = ["/etc/pam.d/system-authand", "/etc/pam.d/password-auth"]
        for path in paths:
            if os.path.isfile(path):
                common.warn("{} exists, needs checking (password lockout)".format(path))

        path = "/etc/pam.d/common-auth"
        common.backup(path)

        with open(path) as in_file:
            lines = in_file.read().split("\n")

        unix_index = None

        # used for fedora based distros
#     text = """auth required pam_tally2.so onerr=fail audit silent deny=5 unlock_time=900
# auth required pam_faillock.so preauth audit silent deny=5 unlock_time=900
# auth sufficient pam_unix.so
# auth [default=die] pam_faillock.so authfail audit deny=5unlock_time=900
# auth sufficient pam_faillock.so authsucc audit deny=5 unlock_time=900"""

        text = """auth required pam_tally2.so onerr=fail audit silent deny=5 unlock_time=900"""

        for index, line in enumerate(lines):
            if "pam_faillock.so" in line:
                common.warn("Found faillock, needs checking (password lockout)")
            elif "pam_unix.so" in line:
                unix_index = index

        if unix_index is not None:
            lines.insert(unix_index, text)
        else:
            common.error("Error {} not formatted as expected".format(path))
            return

        with open(path, "w") as out_file:
            out_file.write("\n".join(lines))

        common.debug("Set Password Lockout")
