from subprocess import Popen, PIPE
from .exceptions import SshException
from .abstract_openssh import AbstractOpenSSH


class Ssh(AbstractOpenSSH):
    """
    Implement in a simple way ssh command
    """
    SSH_COMMAND = "/usr/bin/ssh -i {} -o StrictHostKeyChecking=no {}@{} {}"

    def __init__(self, app=None):
        self.init_app(app)

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
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        output = process.communicate()

        if process.returncode == 1:
            raise Exception(output.decode('utf-8'))
