# CentSecure

[![Build Status](https://ci.jakewalker.xyz/api/badges/malvern-cads/centsecure/status.svg?ref=refs/heads/master)](https://ci.jakewalker.xyz/malvern-cads/centsecure)

CentSecure is a tool for automating *parts* of [CyberCenturion](https://www.cybersecuritychallenge.org.uk/what-we-do/cybercenturion-vi). We are focusing on tasks which are easy (e.g. running a single command) and/or time consumung (e.g. removing backdoors).

> **⚠️ Warning:** Use of this tool when it is open source is against CyberCenturion and CyberPatriot rules. However, you may still use it for inspiration for your own tools.

CyberCenturion is a blue-teaming exercise run by [Cyber Security Challenge UK](https://www.cybersecuritychallenge.org.uk/) which involves securing 3 virtual machines. See more about how it works [here](https://cadscheme.co.uk/cybercenturion/).

CentSecure fixes security holes automatically which gets some of the 'lower hanging fruits' leaving us to focus on some of the harder things. It is designed to work on all platforms and adapt to the platform that it is being run on. Instead of having a bash script for Linux based systems and a batch script for Windows based systems, it makes sense to keep everything in one place.

## Usage

CentSecure doesn't require any configuration or arguments, so you just need to open it and follow the prompts that it gives.

CentSecure can take certain optional command line paramters. These are particularly useful for debugging.
```
usage: centsecure.py [-h] [--list-plugins] [--run-plugin N [N ...]]

Automatically fixes common security vulnerabilities.

optional arguments:
  -h, --help            show this help message and exit
  --list-plugins, -l   Lists all plugins
  --run-plugin N [N ...], -r N [N ...], -p N [N ...]
                        Run specific plugins

Default behaviour is to attempt to run all plugins
```

### Installation Scripts

We have installation scripts for both Ubuntu and Windows which are in the `scripts` folder. Simply clone the repository (or download as a ZIP from GitHub) and run one of the scripts. Both of the installers focus on installing python and the dependencies required for CentSecure.

#### Windows

The batch file installer for Windows *must be* run from an elevated command prompt and *will not* work as intended if run from the file explorer.

### Manual Installation

If you don't want to use the installation scripts, you can manually install CentSecure. Read our [Installation Guide](development/installation.md) for more information on manually installing dependencies.
