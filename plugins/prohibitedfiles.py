"""A plugin to remove prohibited files."""

import plugin
import common
import os
import glob
import shutil


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
    os = ["Windows", "Linux"]
    os_version = ["All"]

    def _get_home_directories(self):
        if "Windows" in plugin.get_os():
            return glob.glob("C:\\Users\\*\\")
        elif "Linux" in plugin.get_os():
            dir_list = glob.glob("/home/*/")

            # This could be damaging so ask first!
            if common.input_yesno("Would you like to clear the root directory too"):
                dir_list.append("/root/")

            return dir_list
        else:
            raise Exception("Unexpected Operating System")

    def _last_folder_name(self, path):
        # Extract the last folder name from a path (e.g. /home/user/ becomes user)
        return os.path.basename(os.path.dirname(path))

    def _clear_folder(self, d):
        for filename in os.listdir(d):
            file_path = os.path.join(d, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def execute(self):
        """Execute plugin."""
        # Fetch a list of home directories
        dirs = self._get_home_directories()
        common.info("Found {} home directories: {}".format(len(dirs), dirs))
        exclude = common.input_list("Please input a list of folder names to exclude (recommended to add your username)")

        for d in dirs:
            if any(e == self._last_folder_name(d) for e in exclude):
                common.debug("Skipping directory {}".format(d))
                continue

            common.info("Purging {}...".format(d))
            common.debug("Backing up folder...")
            common.backup(d, compress=True)

            common.debug("Removing folder contents...")
            self._clear_folder(d)
