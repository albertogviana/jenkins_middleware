from subprocess import Popen, PIPE
from .exceptions import ScpException
from .abstract_openssh import AbstractOpenSSH


class Scp(AbstractOpenSSH):
    """
    Implement in a simple way scp command
    """
    SCP_COMMAND = '/usr/bin/scp -o StrictHostKeyChecking=no -o ConnectTimeout={:d} -i {} -r {} {}@{}:{} 2>&1'

    def __init__(self, app=None, connection_timeout=10):
        self.connection_timeout = connection_timeout
        self.init_app(app)

    def _parse(self, source, destination, host):
        """
        Parse the parameters
        :param source: string
        :param destination:  string
        :param host:  string
        :return: string
        """
        if self.has_app() is False:
            raise ScpException("The OPENSSH_CONFIGURATION parameter was not found, it is required for scp.")

        return self.SCP_COMMAND.format(*[
            self.connection_timeout,
            self.app[self.OPENSSH_CONFIGURATION][self.KEY_FILE],
            source,
            self.app[self.OPENSSH_CONFIGURATION][self.USER],
            self._get_host(host),
            destination
        ])

    def execute(self, source, destination, host):
        """
        Execute the command
        :param source: string
        :param destination: string
        :param host: string
        """
        if source is "":
            raise ScpException("The source parameter could not be empty on scp.")

        if destination is "":
            raise ScpException("The destination parameter could not be empty on scp.")

        if host is "":
            raise ScpException("The host parameter could not be empty on scp.")

        command = self._parse(source, destination, host)
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        output = process.communicate()

        if process.returncode == 1:
            raise Exception(output.decode('utf-8'))
