"""The main file for starting CentSecure.

This code loads payloads from the folder and executes them if they match the host's
operating system.
"""

import payload
from common import is_admin, info, warn, debug, stdout
import sys
import argparse


def get_payloads():
    """Fetches a list of payloads.

    Returns:
        list[str]: A list of name of payloads, with spaces escaped with hyphens

    """
    payloads = []
    for p in payload.Payload._registry:
        name = p.name.replace(" ", "-")
        payloads.append(name)
    return payloads


def run(payloads=[]):
    """Runs the payloads.

    Args:
        payloads (list[str], optional): An option list of specific payloads to run

    """
    all_payloads = payload.Payload._registry

    # Sort payloads in priority order
    all_payloads.sort(key=lambda x: x.priority)

    for p in all_payloads:
        if not payloads or p.name.replace("-", " ") in payloads:
            debug("Payload: {} (targets {} version {}, priority {})".format(p.name, p.os, p.os_version, p.priority))

            if payload.os_check(p.os, p.os_version):
                instance = p()
                info("Running {}...".format(p.name))
                instance.execute()
            else:
                warn("Not running {} as this is not the right OS".format(p.name))
        else:
            warn("Skipping {}".format(p.name))


def main():
    """Main function."""
    # Need to get payloads first for arguments to function
    payload.find_plugins()

    parser = argparse.ArgumentParser(description="Automatically fixes common security vulnerabilities.", epilog="Default behaviour is to attempt to run all payloads")
    parser.add_argument("--list-payloads", "-l", action="store_true", help="Lists all payloads", dest="list_payloads")
    parser.add_argument("--run-payload", "-r", "-p", choices=get_payloads(), nargs="+", metavar="N", help="Run specific payloads", dest="payloads")
    args = parser.parse_args()

    info("Welcome to CentSecure!")
    debug("This computer is running {} version {}".format(payload.get_os(), payload.get_os_version()))

    if args.list_payloads:
        payloads = get_payloads()
        for p in payloads:
            stdout("- {}".format(p))
        sys.exit(1)
    elif is_admin():
        run(args.payloads)
    else:
        warn("CentSecure should be run as root or administator.")
        sys.exit(1)


if __name__ == "__main__":
    main()
