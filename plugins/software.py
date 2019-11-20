"""A plugin for removing and adding software."""

import plugin
import common
import re
import json

# If any of these are matched against:
# - package name on Linux
# - program name, publisher on Windows
# ...then they will be skipped
WHITELIST = ["Microsoft Corporation"]


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
    if common.is_os_64bit():
        registry_key = "HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*"  # 64-bit registry key
    else:
        registry_key = "HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*"  # 32-bit registry key

    output = common.run(["powershell.exe", "Get-ItemProperty {} | Select-Object DisplayName, Publisher, UninstallString | ConvertTo-Json".format(registry_key)])

    try:
        json_output = json.loads(output)
    except json.decoder.JSONDecodeError as ex:
        common.error("Error parsing software list!", ex)
    else:
        return json_output


def _remove_ubuntu_packages(packages):
    package_string = " ".join(packages)
    common.run("apt remove --purge -y {}".format(package_string))
    common.run("apt autoremove -y")


def _check_whitelist(obj):
    if isinstance(obj, dict):
        for k in obj.keys():
            if obj[k] in WHITELIST:
                return True
    elif isinstance(obj, str):
        if obj in WHITELIST:
            return True
    return False


class RemoveSoftwareUbuntu(plugin.Plugin):
    """Remove software packages interactively on Ubuntu and Debian."""
    name = "Remove Software (Ubuntu/Debian)"
    os = ["Ubuntu", "Debian"]
    os_version = ["all"]

    def execute(self):
        """Remove the packages."""
        packages = _list_ubuntu_packages()

        # As this will take lots of manual labour, ask if they would like to check each package.
        check = common.input_yesno("Found {} user-installed packages. Would you like to manually check them".format(len(packages)))

        if check is False:
            return

        to_remove = []
        i = 0
        for package in packages:
            i += 1
            if _check_whitelist(package):
                common.debug("The package {} is being skipped as it is whitelisted.".format(package))
                continue

            keep = common.input_yesno("({}/{}) Would you like to keep the program '{}'".format(i, len(packages), package))
            if not keep:
                to_remove.append(package)

        common.debug("Need to remove {}".format(to_remove))
        confirm = common.input_yesno("Are you sure that you would like to remove {} programs".format(len(to_remove)))

        if not confirm:
            return

        _remove_ubuntu_packages(to_remove)
        common.debug("Removed packages!")


class RemoveSoftwareWindows(plugin.Plugin):
    """Remove software interactively on Windows."""
    name = "Remove Software (Windows)"
    os = ["Windows"]
    os_version = ["all"]

    def execute(self):
        """Remove the packages."""
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

            if _check_whitelist(program):
                common.debug("The program '{}' (by '{}') is being skipped as it is whitelisted.".format(program["DisplayName"], program["Publisher"]))
                continue

            keep = common.input_yesno("({}/{}) Would you like to keep the program '{}' (by '{}')".format(i, len(programs), program["DisplayName"], program["Publisher"]))
            if not keep:
                common.run_full(program["UninstallString"])

        common.debug("Removed packages!")
