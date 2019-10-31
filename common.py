"""
This file contains 'helper' functions that are used in payloads.
"""

import tempfile
import os
import shutil
import datetime
import platform


def _backup_directory():
    """
    Get the backup directory
    """
    directory = os.path.join(tempfile.gettempdir(), "centsecure")
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def _filename(path, t=None):
    d = datetime.datetime.now()
    return ((t + "_") if t is not None else "") + "{}-{}-{}_{}-{}-{}_".format(d.year, d.month, d.day, d.hour, d.minute, d.second) + path.replace("/", "_")[1:]


def backup(source):
    """
    Copy the file at `source` to the backup directory.
    """
    print("Backing up file {}...".format(source))
    dest_filename = _filename(source, "file")
    dest_path = os.path.join(_backup_directory(), dest_filename)
    shutil.copyfile(source, dest_path)
    print("The file {} has been backed up to {}".format(source, dest_path))
    return dest_path


def backup_folder(source):
    """
    Copy the folder at `source` to the backup directory.
    """
    print("Backing up folder {}...".format(source))
    dest_filename = _filename(source, "folder") + (".tar.bz2" if platform.system().lower() == "linux" else ".zip")
    dest_path = os.path.join(_backup_directory(), dest_filename)
    shutil.make_archive(dest_path, ("bztar" if platform.system().lower() == "linux" else "zip"), source)
    print("The folder {} has been compressed and backed up to {}".format(source, dest_path))
    return dest_path
