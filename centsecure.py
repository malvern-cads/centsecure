"""The main file for starting CentSecure.

This code loads plugins from the folder and executes them if they match the host's
operating system.
"""

import plugin
from common import is_admin, info, warn, debug, stdout, reminder
from common import camel_case_to_snake_case, get_default_plugins
import sys
import argparse
import firsttime
from platform import python_version_tuple, python_version


def plugin_slug(p):
    """Generate a plugin slug.

    A slug is used to identify the plugin in a human readable way.

    Args:
        p (str): The plugin to create a slug from

    Returns:
        str: The slug that was generated

    """
    return camel_case_to_snake_case(p.__name__)


def get_plugins():
    """Fetches a list of plugins.

    Returns:
        list[str]: A list of name of plugins, with spaces escaped with hyphens

    """
    plugins = []
    for p in plugin.Plugin._registry:
        name = plugin_slug(p)
        plugins.append(name)
    return plugins


def run(plugins=[]):
    """Runs the plugins.

    Args:
        plugins (list[str], optional): An option list of specific plugins to run

    """
    all_plugins = plugin.Plugin._registry
    failures = []

    # Sort plugins in priority order
    all_plugins.sort(key=lambda x: x.priority)

    for p in all_plugins:
        if plugin_slug(p) in plugins:
            debug("Plugin: {} (targets {} version {}, priority {})".format(p.name, p.os, p.os_version, p.priority))

            if plugin.os_check(p.os, p.os_version):
                instance = p()
                info("Running {}...".format(p.name))

                try:
                    instance.execute()
                except Exception as ex:
                    reminder("The plugin {} failed to run".format(p.name), ex)
                    failures.append(plugin_slug(p))
            else:
                warn("Not running {} as this is not the right OS".format(p.name))
        else:
            warn("Skipping {}".format(p.name))

    reminder("To run all of the failed plugins again, execute CentSecure with the following argument: '-r {}'".format(" ".join(failures)))


def _check_python_version():
    version = python_version_tuple()
    return version[0] == '3' and version[1] == '7'


def main():
    """Main function."""
    # Need to get plugins first for arguments to function
    plugin.find_plugins()

    parser = argparse.ArgumentParser(description="Automatically fixes common security vulnerabilities.", epilog="Default behaviour is to attempt to run all plugins")
    parser.add_argument("--list-plugins", "-l", action="store_true", help="Lists all plugins", dest="list_plugins")
    parser.add_argument("--run-plugin", "-r", "-p", choices=get_plugins(), nargs="+", metavar="N", help="Run specific plugins", dest="plugins")
    parser.add_argument("--run-all", "-R", action="store_true", help="Run all available plugins", dest="run_all")
    parser.add_argument("--disable-root-check", "--no-root", "-d", action="store_true", help="Disable root check", dest="no_root_check")
    parser.add_argument("--disable-python-check", action="store_true", help="Disable Python version check", dest="disable_python_check")
    args = parser.parse_args()

    info("Welcome to CentSecure!")
    debug("This computer is running {} version {}".format(plugin.get_os(), plugin.get_os_version()))

    if args.list_plugins:
        plugins = get_plugins()
        for p in plugins:
            stdout("- {}".format(p))
        sys.exit(0)

    if not args.disable_python_check and not _check_python_version():
        warn("CentSecure requires Python 3.7.x, you are using {}. Use the option --disable-python-check to bypass.".format(python_version()))
        sys.exit(1)

    firsttime.run_all()

    if args.run_all:
        to_run = get_plugins()
    elif args.plugins is not None:
        to_run = args.plugins
    else:
        to_run = get_default_plugins()

    if is_admin() or args.no_root_check:
        debug("Running CentSecure with the following {} plugins: {}".format(len(to_run), ", ".join(to_run)))
        run(to_run)
    else:
        warn("CentSecure should be run as root or administator. Use the option --disable-root-check to bypass.")
        sys.exit(1)


if __name__ == "__main__":
    main()
