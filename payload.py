"""Payload specific code.

Contains the base class for payloads, plugin loaders and OS checking functions.
"""

from importlib import import_module
from pathlib import Path
import platform
from common import debug


def find_plugins():
    """Find payloads in the directory and import them (allowing them to be added to the registry)."""
    import payloads

    for path in payloads.__path__:
        root = Path(path)
        debug("Searching {} for plugins...".format(root))

        for child in root.iterdir():
            if not (child.is_dir() or (child.is_file() and child.suffix == ".py")):
                continue

            rel_path = child.relative_to(root)

            name = ".".join(rel_path.parts[:-1] + (rel_path.stem,))

            try:
                import_module("payloads.{}".format(name))
            except ImportError:
                pass


class Payload:
    """The base class for payloads."""
    _registry = []
    name = "Unknown Payload"
    os = ["all"]
    os_version = ["all"]
    priority = 10  # Lower number means higher priority (can be negative)

    def __init_subclass__(cls, **kwargs):
        """Subclass loader.

        When subclasses (i.e. payloads in the folder are loaded) they are added to the _registry
        list on this class.
        """
        super().__init_subclass__(**kwargs)
        cls._registry.append(cls)

    def execute(self):
        """Function that is run when the payload is executed."""
        raise NotImplementedError


def get_os():
    """Get the host's operating system.

    Returns:
        list[str]: List containing all of the operating systems that the current computer runs.

    """
    os = [platform.system(), "all"]
    if "Linux" in os:
        os.append(platform.linux_distribution()[0])  # i.e. 'Ubuntu'...

    return os


def get_os_version():
    """Get the versions of os that the host is running.

    Returns:
        list[str]: List containing all of the operating system versions that the current computer runs.

    """
    version = [platform.release(), platform.version(), "all"]
    if "Linux" in get_os():
        dist = platform.linux_distribution()
        version.append(dist[1])  # i.e. '18.04', '19.10'...
        version.append(dist[2])  # i.e. 'bionic'...

    return version


def _list_to_lower(l):
    return [x.lower() for x in l]


def _common_items(x, y):
    return list(set(x).intersection(y))


def os_check(target_os, target_os_version):
    """Check a payload's target OS and target OS version against what the computer is running.

    Args:
        target_os (list[str]): List of operating systems that the payload works against.
        target_os_version (list[str]): List of operating system versions that the payload works against.

    Returns:
        bool: Whether the payload will work against this computer.

    """
    target_os = _list_to_lower(target_os)
    target_os_version = _list_to_lower(target_os_version)
    os = _list_to_lower(get_os())
    os_version = _list_to_lower(get_os_version())

    # Check that there is common items in both the (os and target_os) and (os_version and target_os_version) lists
    return len(_common_items(os, target_os)) >= 1 and len(_common_items(os_version, target_os_version)) >= 1
