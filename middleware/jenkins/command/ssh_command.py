import os
from middleware.openssh.ssh import Ssh


class SshCommand(object):

    def __init__(self, app_configuration):
        self.app_configuration = app_configuration
        self.ssh = self.get_ssh_instance()

    def execute(self, host, command):
        print("ssh command")
        self.ssh.execute(host, command)

    def get_ssh_instance(self):
        return Ssh(self.app_configuration["OPENSSH_CONFIGURATION"])
