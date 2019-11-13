"""Common functions for use throughout payloads.

This file contains common functions that can be used throughout CentSecure, mainly
in payloads. There are logging, backup and other functions.

  Logging usage:
  common.debug('Changing passwords...')

  Backup usage:
  backup('/home/user/cat.jpg')
"""

import os
import shutil
import datetime
import platform
import ctypes
from colorama import init, Fore, Back
import subprocess


def _log(text):
    """Appends the message to the log file.

    Args:
        text (str): The text to save

    """
    with open("output.log", "a") as out_file:
        out_file.write("{}\n".format(text))


def stdout(msg):
    """Print command output to the console.

    Args:
        msg (str): The commands stdout

    """
    output = msg.strip()
    _log(output)
    print(output)  # noqa: T001


def info(msg):
    """Print a message to the console containing information.

    Args:
        msg (str): The message to print to the console

    """
    output = "[i] {}".format(msg)
    _log(output)
    print(Fore.BLUE + output)  # noqa: T001


def debug(msg):
    """Print a debugging message to the console.

    This might not always be shown to the user.

    Args:
        msg (str): The message to print to the console

    """
    output = "[#] {}".format(msg)
    _log(output)
    print(Fore.WHITE + output)  # noqa: T001


def warn(msg):
    """Print a warning message to the console.

    Args:
        msg (str): The message to print to the console

    """
    output = "[!] {}".format(msg)
    _log(output)
    print(Fore.YELLOW + output)  # noqa: T001


def error(msg, e=None):
    """Print an error message to the console.

    Args:
        msg (str): The message to print to the console
        e (exception, optional): An exception to show alongside the message. Defaults to None.

    """
    if e is not None:
        output = "[E] {} -> {}".format(msg, repr(e))
    else:
        output = "[E] {}".format(msg)
    print(Fore.WHITE + Back.RED + output)  # noqa: T001
    _log(output)


def input_text(msg):
    """Ask a question to the user and get a text-based response.

    Args:
        msg (str): The question to be asked to the user (without a question mark)

    Returns:
        str: The user's response

    """
    while True:
        question = "[?] {}? ".format(msg)
        user_input = input(Fore.GREEN + question)
        _log(question + user_input)
        return user_input


def input_yesno(msg):
    """Ask a yes or no question to the user and get a boolean response.

    Args:
        msg (str): The question to be asked to the user (without a question mark)

    Returns:
        boolean: The user's response (True for yes, False for no)

    """
    while True:
        user_input = input_text(msg + " (y/n)")
        if user_input.lower() == "y":
            return True
        elif user_input.lower() == "n":
            return False
        else:
            warn("Unexpected input")


def input_list(msg):
    """Ask a question to the user and get a list as a response.

    Args:
        msg (str): The prompt to be shown. (e.g. Write a list of...)

    Returns:
        list[str]: The user's response as a list of strings

    """
    while True:
        output = "[?] {}. Please seperate items with a semicolon.".format(msg)
        print(Fore.GREEN + output)  # noqa: T001
        input_text = "    > "
        user_input = input(Fore.GREEN + input_text)
        _log("{}\n{}{}".format(output, input_text, user_input))
        input_list = user_input.split(";")

        question = "This is what you inputted:\n - {}\nIs that correct".format("\n - ".join(input_list))

        if input_yesno(question):
            return input_list


def is_admin():
    """Check if the user running the script has admin privileges.

    Returns:
        boolean: Whether the user is an admin (True if they are, False if they are not)

    """
    try:
        return os.getuid() == 0
    except AttributeError:
        pass

    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        pass

    return False


def get_current_users():
    """Returns a list of the non-system users on the system.

    Returns:
        list[str]: List containing all of the usernames of non-system users

    """
    with open("/etc/passwd") as in_file:
        text = in_file.read()

    # Format - Username:Password:UID:GID:User ID Info:Home directory:Shell
    user_data = [i.split(":") for i in text.split("\n") if i != ""]
    normal_users = []
    for user in user_data:
        # UID range to be a non-system user
        if 1000 <= int(user[2]) < 60000:
            normal_users.append(user[0])
    return normal_users


def change_parameters(path, params):
    """Modify a config file with the given parameters.

    The config file needs to be in the format: <key> <value>

    Args:
        path (str): The path to the config file to modify
        params (dictionary): A dictionary containing keys and their corresponding values to be modified

    """
    with open(path) as in_file:
        lines = in_file.read().split("\n")

    # Grab location in file of keys
    indices = {}
    for index, line in enumerate(lines):
        # Ensure we grab the key
        key_word = line.split(" ")[0]
        if key_word in params:
            indices[key_word] = index

    for param in params:
        # Format of config file
        line = "{0} {1}".format(param, params[param])
        if param in indices:
            index = indices[param]
            lines[index] = line
        else:
            # If the key isn't in the file, we append it to the end
            lines.append(line)

    with open(path, "w") as out_file:
        out_file.write("\n".join(lines))
        out_file.write("\n")


def _backup_directory():
    """Generate a folder where backups should be stored.

    Returns:
        str: Path to the backup folder

    """
    directory = "backups"
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def _filename(path, t=None):
    """Generate a filename for a backed up file.

    Args:
        path (str): The path where the file originated from
        t (str, optional): The type of file (file or folder). Defaults to None.

    Returns:
        str: The filename

    """
    d = datetime.datetime.now()
    return ((t + "_") if t is not None else "") + "{}-{}-{}_{}-{}-{}_".format(d.year, d.month, d.day, d.hour, d.minute, d.second) + path.replace("/", "_")[1:]


def backup(source, compress=False):
    """Copy the file or folder from the source to the backup directory.

    Args:
        source (str): A path to the file or folder to backup
        compress (bool, optional): Whether the folder should be compressed. Defaults to False.

    Returns:
        str: The path of where the file or folder was backed up to

    """
    # Check if the source path is a folder or not
    folder = os.path.isdir(source)
    backup_type = "folder" if folder else "file"
    debug("Backing up {} {}...".format(backup_type, source))

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
    info("The {} {} has been{} backed up to {}".format(backup_type, source, (" compressed and" if compress and folder else ""), dest_path))
    return dest_path


def run(cmd, include_error=False):
    """Run a shell command.

    Args:
        cmd (str/list[str]): The command to be run.
        include_error (bool): Option to include error output in return variable.

    Returns:
        str: The command's output.

    """
    stderr = subprocess.STDOUT if include_error else None
    command_list = cmd if isinstance(cmd, list) else cmd.split(" ")
    debug("Running command '{}'".format(cmd))
    result = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=stderr)
    return result.stdout.decode("utf-8")


def run_full(cmd, include_error=False):
    """Run a shell command unescaped and with bash.

    Args:
        cmd (str): The command to be run.
        include_error (bool): Option to include error output in return variable.

    Returns:
        str: The command's output

    """
    stderr = subprocess.STDOUT if include_error else None
    warn("Running unescaped command '{}'".format(cmd))
    # Full commands are likely to be complex so we run using bash instead of sh
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=stderr, executable="/bin/bash")
    return result.stdout.decode("utf-8")


# Initialize colorama
init(autoreset=True)
