import os
import payload
import common


class LinuxAccountManagement(payload.Payload):
    name = "Linux Account Management"
    os = ["Linux"]
    os_version = ["ALL"]

    def execute(self):
        common.backup("/etc/passwd")
        common.backup("/etc/group")
        common.backup("/etc/shadow")

        current_user = common.input_text("What is the current username")

        admins = self.get_users("Admin")
        # ensures the current user isn't in the admin list
        if current_user in admins:
            admins.remove(current_user)

        standard = self.get_users("Standard")
        # ensures the current user isn't in the standard list
        if current_user in standard:
            standard.remove(current_user)

        current_users = common.get_current_users()

        # first we need to get rid of the bad users
        bad_users = []
        for user in current_users:
            if user not in current_user + admins + standard:
                bad_users.append(user)
        self.delete_users(bad_users)

        current_users = list(set(current_users) - set(bad_users))

        # find new users
        new_users = []
        for user in admins + standard:
            if user not in current_users:
                new_users.append(user)
        self.create_users(new_users)

        # set all users to a standard user
        self.set_standard_users(standard)
        # set admin users to admin
        self.set_admin_users(admins)

        # change password to a secure one
        common.info("Changing passwords")
        for index, user in enumerate(admins + standard):
            password = "CyberCenturion{}!".format(index)
            self.change_password(user, password)

    def get_users(self, rank="standard"):
        return common.input_list("Enter a list of {} users".format(rank.lower()))

    def delete_users(self, users):
        for user in users:
            # TODO backup user directory
            # TODO find any other files elsewhere in the system that user owns
            os.system("crontab -r -u {}".format(user))
            os.system("userdel -r {}".format(user))
            common.info("Deleted user {}".format(user))

    def create_users(self, users):
        for user in users:
            os.system("useradd -s /bin/bash -m {}".format(user))
            common.info("Added user {}".format(user))

    def set_standard_users(self, users):
        for user in users:
            # set only group to be the user's primary group
            os.system("usermod -G {0} {0}".format(user))
            common.info("Removed all groups from user {}".format(user))

    def set_admin_users(self, users):
        for user in users:
            # first remove all groups
            os.system("usermod -G {0} {0}".format(user))
            # list of groups we want to add the user to
            admin_roles = ["sudo"]
            # add the admin roles
            os.system("usermod -aG {0} {1}".format(", ".join(admin_roles), user))

    def change_password(self, user, password):
        os.system("echo '{0}:{1}' | chpasswd".format(user, password))
        common.info("Changing password of {0} to {1}".format(user, password))
