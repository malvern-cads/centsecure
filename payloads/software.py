import payload
import common
import re
import json


def _list_ubuntu_packages():
    output = common.run("apt list --installed")
    package_list = output.split("\n")
    packages = []

    for p in package_list:
        p = p.strip()

        # Skip empty package names or the string 'Listing...'
        if p == "" or p == "Listing...":
            continue

        if re.search(r".*\/.* \[.*\]", p) is None:
            common.warn("Unexpected package: {}".format(p))
            continue

        # Get text up to first '/' (package name)
        name = p.partition("/")[0]
        # Get package flags
        flags = re.search(r".*\/.* \[(.*)\]", p).group(1).split(",")

        # If the package was installed automatically (i.e. system package OR dependency)
        if "automatic" in flags:
            continue

        packages.append(name)

    return packages


def _list_windows_programs():
    output = common.run(["powershell.exe", "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName, Publisher, UninstallString | ConvertTo-Json"])
    return json.loads(output)


def _remove_ubuntu_packages(packages):
    package_string = " ".join(packages)
    common.run("apt remove --purge -y {}".format(package_string))
    common.run("apt autoremove -y")


class RemoveSoftwareUbuntu(payload.Payload):
    name = "Remove Software (Ubuntu)"
    os = ["Ubuntu"]
    os_version = ["all"]

    def execute(self):
        packages = _list_ubuntu_packages()

        # As this will take lots of manual labour, ask if they would like to check each package.
        check = common.input_yesno("Found {} user-installed packages. Would you like to manually check them".format(len(packages)))

        if check is False:
            return

        to_remove = []
        i = 0
        for package in packages:
            i += 1

            keep = common.input_yesno("({}/{}) Would you like to keep the program '{}'".format(i, len(packages), package))
            if not keep:
                to_remove.append(package)

        common.debug("Need to remove {}".format(to_remove))
        confirm = common.input_yesno("Are you sure that you would like to remove {} programs".format(len(to_remove)))

        if not confirm:
            return

        _remove_ubuntu_packages(to_remove)
        common.debug("Removed packages!")


class RemoveSoftwareWindows(payload.Payload):
    name = "Remove Software (Windows)"
    os = ["Windows"]
    os_version = ["all"]

    def execute(self):
        programs = _list_windows_programs()

        # As this will take lots of manual labour, ask if they would like to check each program.
        check = common.input_yesno("Found {} programs. Would you like to manually check them".format(len(programs)))

        if check is False:
            return

        i = 0
        for program in programs:
            i += 1

            if program["UninstallString"] is None:
                common.warn("The program '{}' (by '{}') cannot be automatically removed. If it is of concern please remove it manually.".format(program["DisplayName"], program["Publisher"]))
                continue


            keep = common.input_yesno("({}/{}) Would you like to keep the program '{}' (by '{}')".format(i, len(programs), program["DisplayName"], program["Publisher"]))
            if not keep:
                common.run(program["UninstallString"])

        common.debug("Removed packages!")
