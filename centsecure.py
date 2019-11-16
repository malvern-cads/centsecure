"""The main file for starting CentSecure.

This code loads plugins from the folder and executes them if they match the host's
operating system.
"""

import plugin
from common import is_admin, info, warn, debug, stdout
import sys
import argparse
import firsttime


def get_plugins():
    """Fetches a list of plugins.

    Returns:
        list[str]: A list of name of plugins, with spaces escaped with hyphens

    """
    plugins = []
    for p in plugin.Plugin._registry:
        name = p.name.replace(" ", "-")
        plugins.append(name)
    return plugins


def run(plugins=[]):
    """Runs the plugins.

    Args:
        plugins (list[str], optional): An option list of specific plugins to run

    """
    all_plugins = plugin.Plugin._registry

    # Sort plugins in priority order
    all_plugins.sort(key=lambda x: x.priority)

    for p in all_plugins:
        if not plugins or p.name.replace(" ", "-") in plugins:
            debug("Plugin: {} (targets {} version {}, priority {})".format(p.name, p.os, p.os_version, p.priority))

            if plugin.os_check(p.os, p.os_version):
                instance = p()
                info("Running {}...".format(p.name))
                instance.execute()
            else:
                warn("Not running {} as this is not the right OS".format(p.name))
        else:
            warn("Skipping {}".format(p.name))


def main():
    """Main function."""
    # Need to get plugins first for arguments to function
    plugin.find_plugins()

    parser = argparse.ArgumentParser(description="Automatically fixes common security vulnerabilities.", epilog="Default behaviour is to attempt to run all plugins")
    parser.add_argument("--list-plugins", "-l", action="store_true", help="Lists all plugins", dest="list_plugins")
    parser.add_argument("--run-plugin", "-r", "-p", choices=get_plugins(), nargs="+", metavar="N", help="Run specific plugins", dest="plugins")
    args = parser.parse_args()

    info("Welcome to CentSecure!")
    debug("This computer is running {} version {}".format(plugin.get_os(), plugin.get_os_version()))

    if args.list_plugins:
        plugins = get_plugins()
        for p in plugins:
            stdout("- {}".format(p))
        sys.exit(0)

    firsttime.run_all()

    if is_admin():
        run(args.plugins)
    else:
        warn("CentSecure should be run as root or administator.")
        sys.exit(1)


if __name__ == "__main__":
    main()
