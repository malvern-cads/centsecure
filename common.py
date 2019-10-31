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


def backup(source, compress=False):
    """
    Copy the file at `source` to the backup directory.
    """
    # Check if the source path is a folder or not
    folder = os.path.isdir(source)
    backup_type = "folder" if folder else "file"
    print("Backing up {} {}...".format(backup_type, source))

    # Generate a filename from the source path
    dest_filename = _filename(source, backup_type)
    # Append the filename from above onto the end of the backup directory
    dest_path = os.path.join(_backup_directory(), dest_filename)

    # If we are backing up a folder and it should be compressed
    if compress and folder:
        # Use a .tar.bz2 for Linux (higher compression) or if not use a .zip (lower compression)
        compress_type = "bztar" if platform.system().lower() == "linux" else "zip"
        # Get the file extension depending on the compression type
        file_ext = ".tar.bz2" if compress_type == "bztar" else ".zip"
        # Add the file extension to the path
        dest_path += file_ext
        # Copy the folder to the archive
        shutil.make_archive(dest_path, compress_type, source)
    else:
        if not folder:
            # Copy the source file to the destination
            shutil.copy2(source, dest_path)
        else:
            # Copy the source folder to the destination
            shutil.copytree(source, dest_path)
    print("The {} {} has been{} backed up to {}".format(backup_type, source, (" compressed and" if compress and folder else ""), dest_path))
    return dest_path
