# common.py

`common.py` is a small library that we have created to house some common functions that are used throughout CentSecure payloads. _If there is a function in here, please try and use it rather than implementing it your own way, it means we can change something in one place rather than updating it in multiple files._

## Methods

### Logging

- `common.info("Hello")`
- `common.debug("Doing this thing")`
- `common.warn("You don't want to do that!")`
- `common.error("Houston, there's a problem!")`
- `common.error("Houston, there's a problem!", exception)` - *pass an additional parameter for the exception*

### User Input

- `common.input_text("What is your name")` - *question without the question mark*
- `common.input_yesno("Do you want to do this")` - *question without the question mark*
- `common.input_list("Enter a list of your favourite flavours")` - *imperative*

### Backup

- `common.backup("/etc/passwd")`
- `common.backup("/home/jeff", compress=True)`

### Miscellaneous

- `common.get_current_users()` - *Linux only*