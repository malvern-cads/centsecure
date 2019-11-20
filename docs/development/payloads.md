# Plugins

CentSecure is built around 'plugins' which are modules/plugins which do **one** action, for example: configure the firewall, create a user, etc...

These plugins are then loaded into the application when it is run by searching through the `plugins` folder. Each of the plugins is then checked against the OS and OS version of the computer and then it is run.

The `plugins` folder can contain any amount of Python files each containing any number of plugins (Python files cannot be in subfolders, but can be named anything). **It is worth using a naming scheme for Python files so that they can be easily found!**

Each of the Python files can have any number of 'plugins' inside them. Plugins are essentially classes which inherit a base class. This ensures that the `execute()` function always exists. Here is an example of what might be contained in a Python file:

```python
import plugin


class MyPlugin(plugin.Plugin):
    name = "My Plugin"
    os = ["Windows"]
    os_version = ["10"]

    def execute(self):
        # Put code here (e.g. configure firewall, create user, etc...)
```

**Note:** _Each `class` must have a unique name!_

## Plugin Parameters

Plugin parameters help the program to tell which operating systems your plugin should run on. With the plugin example above there are 3 parameters set `name`, `os` and `os_version`, this tells the program that the plugin should only be run on **Windows** operating systems on version **10** only. Here are all of the available plugin parameters:

- **`name`** is just the name that is used when talking about the plugin in the output. It doesn't really matter.
- **`os`** is the operating system that the plugin is targeting. It is a **list** containing all of the operating systems that this plugin is compatible with. (e.g. `all`, `Windows`, `Linux`, `Ubuntu`, etc...)
- **`os_version`** is the version of the operating system that the plugin is targeting. It is also a **list** containing all of the versions of operating system that this plugin is compatible with. (e.g. `all`, `10`, `9`, `19.10`, etc...)
- **`priority`** can help you to configure what order plugins run in. The default is `10` and a lower number dictates a **higher priority**, priorities can also be negative.

> **It is best to run CentSecure on the actual computer that you want the plugin to run on and then copy down the OS and OS version that it prints at the start.**