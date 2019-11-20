"""Functions for setting up CentSecure for the first time."""

import urllib.request
import os.path
import common
import sys


def download_user_js():
    """Download the user.js file if it does not exist."""
    if not os.path.exists("user.js"):
        common.debug("Downloading user.js...")

        user_js_url = "https://raw.githubusercontent.com/ghacksuserjs/ghacks-user.js/master/user.js"
        common.download_file(user_js_url, "user.js")


def run_all():
    """Run all of the first-time functions."""
    common.debug("Running setup...")
    download_user_js()
