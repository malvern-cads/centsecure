"""Functions for setting up CentSecure for the first time."""

import urllib.request
import os.path
import common
import sys


def download_user_js():
    """Download the user.js file if it does not exist."""
    if not os.path.exists("user.js"):
        common.debug("Downloading user.js...")

        user_js_url = "https://raw.githubusercontent.com/ghacksuserjs/ghacks-user.js/v69.0-beta/user.js"

        try:
            urllib.request.urlretrieve(user_js_url, "user.js")
        except urllib.error.URLError as ex:
            common.error("There was a problem downloading user.js. You will need to download it manually from '{}'.".format(user_js_url), ex)
            sys.exit(1)


def run_all():
    """Run all of the first-time functions."""
    common.debug("Running setup...")
    download_user_js()
