# CentSecure

[![Build Status](https://ci.jakewalker.xyz/api/badges/jake-walker/centsecure/status.svg?ref=refs/heads/master)](https://ci.jakewalker.xyz/jake-walker/centsecure)

CentSecure is a tool for automating *parts* of [CyberCenturion](https://www.cybersecuritychallenge.org.uk/what-we-do/cybercenturion-vi). We are focusing on tasks which are easy (e.g. running a single command) and/or time consumung (e.g. removing backdoors).

> **⚠️ Warning:** Use of this tool when it is open source is against CyberCenturion and CyberPatriot rules. However, you may still use it for inspiration for your own tools.

CyberCenturion is a blue-teaming exercise run by [Cyber Security Challenge UK](https://www.cybersecuritychallenge.org.uk/) which involves securing 3 virtual machines. See more about how it works [here](https://cadscheme.co.uk/cybercenturion/).

CentSecure fixes security holes automatically which gets some of the 'lower hanging fruits' leaving us to focus on some of the harder things. It is designed to work on all platforms and adapt to the platform that it is being run on. Instead of having a bash script for Linux based systems and a batch script for Windows based systems, it makes sense to keep everything in one place.

## Usage

CentSecure doesn't require any configuration or arguments, so you just need to open it and follow the prompts that it gives.

### Installation Scripts

We have installation scripts for both Ubuntu and Windows which are in the `scripts` folder. Simply clone the repository (or download as a ZIP from GitHub) and run one of the scripts.

### Manual Installation

If you don't want to use the installation scripts, you can manually install CentSecure. Read our [Installation Guide](docs/development/installation.md) for more information on manually installing dependencies.
