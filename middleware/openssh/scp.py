from subprocess import Popen, PIPE
from urllib.parse import urlparse
from middleware.openssh.interface.openssh import Openssh
from middleware.openssh.exception.openssh_exception import ScpException


class Scp(Openssh):
    SCP_COMMAND = '/usr/bin/scp -o StrictHostKeyChecking=no -o ConnectTimeout={:d} -i {} -r {} {}@{}:{} 2>&1'

    def __init__(self, configuration: {}, connection_timeout=10):
        self.connection_timeout = connection_timeout
        self.configuration = configuration

        if "user" not in self.configuration:
            raise ScpException("User parameter is required for scp.")

        if "key_file" not in self.configuration:
            raise ScpException("Key file is required for scp.")

    @classmethod
    def _get_host(cls, host):
        hostname = urlparse(host)

        if hostname.netloc is "":
            raise ScpException("The host " + host + " informed is not valid for scp.")

        return hostname.netloc

    def _parse(self, source, destination, host):
        """
        Parse the parameters
        :param source: string
        :param destination:  string
        :param host:  string
        :return: string
        """
        return self.SCP_COMMAND.format(*[
            self.connection_timeout,
            self.configuration["key_file"],
            source,
            self.configuration["user"],
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
        print(command)
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        output = process.communicate()

        if process.returncode == 1:
            raise Exception(output.decode('utf-8'))
