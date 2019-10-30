"""
This file contains 'helper' functions that are used in payloads.
"""

import tempfile
import os
import shutil
import datetime


def _backup_directory():
    """
    Get the backup directory
    """
    return os.path.join(tempfile.gettempdir(), "centsecure")


def backup(source):
    """
    Copy the file at `source` to the backup directory.
    """
    d = datetime.datetime.now()
    dest_filename = "{}-{}-{}_{}-{}-{}_".format(d.year, d.month, d.day, d.hour, d.minute, d.second) + source.replace("/", "_")[1:]
    dest_path = os.path.join(_backup_directory(), dest_filename)
    print("{} has been backed up to {}".format(source, dest_path))
    return dest_path