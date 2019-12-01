"""A plugin to remove prohibited files."""

import plugin
import common
import os
import glob


class RemoveMedia(plugin.Plugin):
    """Remove prohibited files."""
    name = "Remove Media"
    os = ["All"]
    os_version = ["All"]

    def execute(self):
        """Execute plugin."""
        if not common.input_yesno("Do you want to search prohibited files"):
            return

        files = self._get_files()

        # As this will take lots of manual labour, ask if they would like to check each file
        check = common.input_yesno("Found {} media files. Would you like to manually check them".format(len(files)))

        if check is False:
            return

        to_remove = []
        for index, f in enumerate(files):
            keep = common.input_yesno("({}/{}) Would you like to keep the file '{}'".format(index + 1, len(files), f))
            if not keep:
                to_remove.append(f)

        common.debug("Need to remove {}".format(to_remove))
        confirm = common.input_yesno("Are you sure that you would like to remove {} media files".format(len(to_remove)))

        if not confirm:
            return

        self._remove_media(to_remove)
        common.debug("Removed media files!")

    def _get_files(self):
        extensions = ["aac", "ac3", "avi", "aiff", "bat", "bmp", "exe", "flac", "gif", "jpeg", "jpg", "mov", "m3u", "m4p",
                      "mp2", "mp3", "mp4", "mpeg4", "midi", "msi", "ogg", "png", "txt", "sh", "wav", "wma", "vqf"]

        common.warn("Only searching for prohibited files in user directories!")
        if "Linux" in plugin.get_os():
            directory = "/home"
        elif "Windows" in plugin.get_os():
            directory = "C:\\Users"
        else:
            return []

        common.info("Searching {} for prohibited files. This may take a while...")

        files = []

        for extension in extensions:
            x = glob.glob(os.path.join(directory, "**/*." + extension), recursive=True)
            files.extend(x)

        return files

    def _remove_media(self, to_remove):
        for media in to_remove:
            os.remove(media)
            common.debug("Removed {}".format(media))


class PurgeHomeDirectories(plugin.Plugin):
    """Purge home directories."""
    name = "Purge Home Directories"
    os = ["All"]
    os_version = ["All"]

    def _get_home_directories(self):
        return glob.glob("/home/*/")

    def execute(self):
        """Execute plugin."""
        # Fetch a list of home directories
        dirs = self._get_home_directories()
        common.info("Found {} home directories: {}".format(len(dirs), dirs))
        exclude = common.input_list("Please input a list of strings to exclude")

        for d in dirs:
            if any(e in d for e in exclude):
                common.debug("Skipping directory {}".format(d))
                continue

            common.info("Purging {}...".format(d))
            common.debug("Backing up folder...")
            common.backup(d, compress=True)

            common.debug("Removing folder contents...")
            for root, dirs, files in os.walk(d, topdown=False):
                for f in files:
                    path = os.path.join(root, f)
                    common.debug("Removing file {}...".format(path))
                    os.remove(path)
                for di in dirs:
                    path = os.path.join(root, di)
                    common.debug("Removing folder {}...".format(path))
                    os.rmdir(path)
