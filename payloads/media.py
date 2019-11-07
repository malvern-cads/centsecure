import payload
import common
import os


class RemoveMedia(payload.Payload):
    name = "Remove Media"
    os = ["All"]
    os_version = ["All"]

    def execute(self):
        files = self.get_files()

        # As this will take lots of manual labour, ask if they would like to check each file
        check = common.input_yesno("Found {} media files. Would you like to manually check them".format(len(files)))

        if check is False:
            return

        to_remove = []
        for index, f in enumerate(files):
            keep = common.input_yesno("({}/{}) Would you like to keep the file '{}'".format(index+1, len(files), f))
            if not keep:
                to_remove.append(f)

        common.debug("Need to remove {}".format(to_remove))
        confirm = common.input_yesno("Are you sure that you would like to remove {} media files".format(len(to_remove)))

        if not confirm:
            return

        self.remove_media(to_remove)
        common.debug("Removed media files!")

    def get_files(self):
        extensions = ["mp3", "mp4", "jpg"]
        if "Linux" in payload.get_os():
            common.warn("Only searching for media files in the /home directory")
            string = " -o ".join(['-iname "*.{}"'.format(i) for i in extensions])
            output = common.run_full('find /home {} 2>/dev/null'.format(string))
            files = [f for f in output.split("\n") if f != ""]
        elif "Windows" in payload.get_os():
            pass

        return files

    def remove_media(self, to_remove):
        for media in to_remove:
            if "Linux" in payload.get_os():
                os.remove(media)
                common.debug("Removed {}".format(media))
            elif "Windows" in payload.get_os():
                pass
