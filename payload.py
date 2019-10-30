from importlib import import_module
from pathlib import Path
from logzero import logger
import platform


def find_plugins():
    import payloads

    for path in payloads.__path__:
        root = Path(path)
        logger.debug("Searching %s for plugins...", root)

        for child in root.iterdir():
            if not (child.is_dir() or (child.is_file() and child.suffix == ".py")):
                continue

            rel_path = child.relative_to(root)

            name = ".".join(rel_path.parts[:-1] + (rel_path.stem,))

            try:
                import_module("payloads.{}".format(name))
            except ImportError:
                pass
            else:
                logger.debug("Loaded plugin: %s", name)


class Payload:
    _registry = []
    name = "Unknown Payload"
    os = ["all"]
    os_version = ["all"]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry.append(cls)

    def execute(self):
        raise NotImplementedError


def get_os():
    os = [platform.system(), "all"]
    if "Linux" in os:
        os.append(platform.linux_distribution()[0])  # i.e. 'Ubuntu'...

    return os


def get_os_version():
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
    target_os = _list_to_lower(target_os)
    target_os_version = _list_to_lower(target_os_version)
    os = _list_to_lower(get_os())
    os_version = _list_to_lower(get_os_version())

    # Check that there is common items in both the (os and target_os) and (os_version and target_os_version) lists
    return len(_common_items(os, target_os)) >= 1 and len(_common_items(os_version, target_os_version)) >= 1
