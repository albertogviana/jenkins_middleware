from subprocess import Popen, PIPE
from urllib.parse import urlparse
from middleware.openssh.exception.openssh_exception import SshException


class Ssh(object):
    SSH_COMMAND = "ssh -i {} -o StrictHostKeyChecking=no {}@{} {}"

    def __init__(self, configuration: {}):
        self.configuration = configuration

        if "user" not in self.configuration:
            raise SshException("User parameter is required for scp.")

        if "key_file" not in self.configuration:
            raise SshException("Key file is required for scp.")

    @classmethod
    def _get_host(cls, host):
        hostname = urlparse(host)

        if hostname.netloc is "":
            raise SshException("The host " + host + " informed is not valid for scp.")

        return hostname.netloc

    def _parse(self, host, shell_script):
        """
        Parse the parameters
        :param host:  string
        :param shell_script:  string
        :return: string
        """
        return self.SSH_COMMAND.format(*[
            self.configuration["key_file"],
            self.configuration["user"],
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
            raise SshException("The host parameter could not be empty on scp.")

        if shell_script is "":
            raise SshException("The shell script parameter could not be empty on scp.")

        command = self._parse(host, shell_script)
        print(command)
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        output = process.communicate()

        if process.returncode == 1:
            raise Exception(output.decode('utf-8'))
