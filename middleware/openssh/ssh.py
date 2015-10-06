from subprocess import Popen, PIPE
from urllib.parse import urlparse
from .exceptions import SshException


class Ssh(object):
    SSH_COMMAND = "/usr/bin/ssh -i {} -o StrictHostKeyChecking=no {}@{} {}"
    OPENSSH_CONFIGURATION = "OPENSSH_CONFIGURATION"
    KEY_FILE = "key_file"
    USER = "user"

    def __init__(self, app=None):

        self.app = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        print(self.app)
        if self.OPENSSH_CONFIGURATION not in self.app:
            raise SshException("The OPENSSH_CONFIGURATION parameter was not found, it is required for ssh.")

        if self.USER not in self.app[self.OPENSSH_CONFIGURATION]:
            raise SshException("User parameter is required for ssh.")

        if self.KEY_FILE not in self.app[self.OPENSSH_CONFIGURATION]:
            raise SshException("Key file is required for ssh.")

    def has_app(self):
        if self.app is None:
            return False

        return True

    @classmethod
    def _get_host(cls, host):
        hostname = urlparse(host)

        if hostname.netloc is "":
            raise SshException("The host " + host + " informed is not valid for ssh.")

        return hostname.netloc

    def _parse(self, host, shell_script):
        """
        Parse the parameters
        :param host:  string
        :param shell_script:  string
        :return: string
        """

        if self.has_app() is False:
            raise SshException("The OPENSSH_CONFIGURATION parameter was not found, it is required for ssh.")

        return self.SSH_COMMAND.format(*[
            self.app[self.OPENSSH_CONFIGURATION][self.KEY_FILE],
            self.app[self.OPENSSH_CONFIGURATION][self.USER],
            self._get_host(host),
            shell_script
        ])

    def execute(self, host, shell_script):
        """
        Execute the command
        :param host: string
        :param shell_script:  string
        """
        if host is "":
            raise SshException("The host parameter could not be empty on ssh.")

        if shell_script is "":
            raise SshException("The shell script parameter could not be empty on ssh.")

        command = self._parse(host, shell_script)
        print(command)
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        output = process.communicate()

        if process.returncode == 1:
            raise Exception(output.decode('utf-8'))
