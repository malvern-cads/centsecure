# Installation

CentSecure requires **[Python 3.7](https://www.python.org/downloads/)** and [pip](https://pypi.org/project/pip/) for Python 3.7.

## Using pipenv

All of CentSecures dependencies are managed by `pipenv`, this makes a [virtual environment](https://docs.python.org/3/tutorial/venv.html) for the CentSecure allowing it to have the same dependencies and Python version installed no matter which computer is running on.

```bash
curl https://pyenv.run | bash # Optionally install pyenv to install the recommended version of Python automatically
python3 -m pip install --user pipenv
```

Now clone the repository to your computer and install the dependencies:

```bash
git clone https://github.com/malvern-cads/centsecure
pipenv install --dev
```

Then to run the program, simply use the command:

```bash
pipenv run python centsecure.py
```

## Using regular pip

If you don't want to use `pipenv`, you can manually install dependencies. Follow the instructions from the section above to clone the repository to your computer, then open `Pipfile` and look under the `[packages]` section and install all of the packages listed there using pip. For example, for `colorama`, you would do:

```bash
python3 -m pip install colorama
```