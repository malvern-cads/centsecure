"""The main file for starting CentSecure.

This code loads payloads from the folder and executes them if they match the host's
operating system.
"""

import payload
from common import is_admin, info, warn, debug
import sys

payloads = {}

info("Welcome to CentSecure!")
debug("This computer is running {} version {}".format(payload.get_os(), payload.get_os_version()))

if not is_admin():
    warn("CentSecure should be run as root or administator.")
    sys.exit(1)

payload.find_plugins()
for p in payload.Payload._registry:
    debug("Payload: {} (targets {} version {})".format(p.name, p.os, p.os_version))

    if payload.os_check(p.os, p.os_version):
        instance = p()
        info("Running {}...".format(p.name))
        instance.execute()
    else:
        warn("Not running {} as this is not the right OS".format(p.name))
