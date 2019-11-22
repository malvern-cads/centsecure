# common.py

`common.py` is a small library that we have created to house some common functions that are used throughout CentSecure plugins. _If there is a function in here, please try and use it rather than implementing it your own way, it means we can change something in one place rather than updating it in multiple files._

## Methods

### Logging

- `common.stdout(common.run("net user admin minad"))` - *used to output information from shell commands*
- `common.info("Hello")`
- `common.debug("Doing this thing")`
- `common.warn("You don't want to do that!")`
- `common.error("Houston, there's a problem!")`
- `common.error("Houston, there's a problem!", exception)` - *pass an additional parameter for the exception*
- `common.reminder("Remember to close the fridge!")` - *save a message until the program has finished running*

### User Input

- `common.input_text("What is your name")` - *question without the question mark*
- `common.input_yesno("Do you want to do this")` - *question without the question mark*
- `common.input_list("Enter a list of your favourite flavours")` - *imperative*

### Backup

- `common.backup("/etc/passwd")`
- `common.backup("/home/jeff", compress=True)`

### Running System Commands

- `common.run(cmd, include_error=True)`
- `common.run_full(cmd, include_error=True)` - *For an unparameterized command, Linux only, the recommended Windows alternative for this is `os.system()`*

### Miscellaneous

- `common.get_current_users()` - *Linux only*
- `common.is_admin()`
- `change_parameters(path, params)`
  - This is used for modifying config files in the format \<key\> \<value\>, where path is the path of the file and params is a dictionary of the keys with their updated values. If the key cannot be found within the file then it is appened to the end of the config file
