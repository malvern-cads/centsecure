from logzero import logger
import payload
import importlib
from common import is_admin
import sys
from os.path import basename, dirname, join
from glob import glob

payloads = {}

logger.info("Welcome to CentSecure!")
logger.info("This computer is running:\n    OS: %s\n    OS Version: %s", payload.get_os(), payload.get_os_version())

if not is_admin():
    logger.warning("CentSecure should be run as root or administator.")
    sys.exit(1)

payload.find_plugins()
for p in payload.Payload._registry:
    logger.info("Module %s:\n    Name: %s\n    Targets: %s (version %s)", p.__name__, p.name, p.os, p.os_version)

    if payload.os_check(p.os, p.os_version):
        instance = p()
        logger.debug("Running %s...", p.__name__)
        instance.execute()
    else:
        logger.debug("Not running %s as this is not the right OS", p.__name__)