import platform
from logzero import logger
import payload
import importlib

from os.path import basename, dirname, join
from glob import glob

payloads = {}

logger.info("Welcome to CentSecure!")
logger.info("This computer is running:\n    Platform: %s\n    Release: %s\n    Version: %s", platform.system(), platform.release(), platform.version())

payload.find_plugins()
for p in payload.Payload._registry:
    logger.info("Module %s:\n    Name: %s\n    Targets: %s (version %s)", p.__name__, p.name, p.os, p.os_version)
    # Do OS Check
    i = p()
    i.execute()