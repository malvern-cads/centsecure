# Tests

This project has checks run against it to check for consistent and clean style. These tests are run against every commit and pull request, but if you are making contributions, you should run them yourself **before committing**!

As well as the 'usual' style linting from `flake8`, we have opted to:

- Disable checks for maximum line lengths
- Enable checks for usage of `print` - you should be using `common.debug`, `common.log`, `common.warn` or `common.error`
- Enable checks for 'dead' code, including commented out code - we are using git so if we need to revert a change we can 😉
- Enable checks for 'docstrings', we are using the Google format (read about the syntax [here](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)) - this makes the code more readable

You can run the tests by running the command `flake8`. _Make sure that you have installed the packages under the `[dev-packages]` section of the Pipfile if you have installed the packages manually!_