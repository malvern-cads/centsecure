from importlib import import_module
from pathlib import Path
from logzero import logger


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
                import_module(f"payloads.{name}")
            except ImportError:
                pass
            else:
                logger.debug("Loaded plugin: %s", name)


class Payload:
    _registry = []
    name = "Unknown Payload"
    os = "all"
    os_version = "all"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry.append(cls)

    def execute(self):
        raise NotImplementedError
