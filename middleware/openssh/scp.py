from subprocess import Popen, PIPE
from urllib.parse import urlparse
from .exceptions import ScpException


class Scp(object):
    SCP_COMMAND = '/usr/bin/scp -o StrictHostKeyChecking=no -o ConnectTimeout={:d} -i {} -r {} {}@{}:{} 2>&1'
    OPENSSH_CONFIGURATION = "OPENSSH_CONFIGURATION"
    KEY_FILE = "key_file"
    USER = "user"

    def __init__(self, app=None, connection_timeout=10):
        self.app = None
        self.connection_timeout = connection_timeout

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize the class configuration
        :param app:
        :return:
        """
        self.app = app

        if self.OPENSSH_CONFIGURATION not in self.app:
            raise ScpException("The OPENSSH_CONFIGURATION parameter was not found, it is required for scp.")

        if self.USER not in self.app[self.OPENSSH_CONFIGURATION]:
            raise ScpException("User parameter is required for scp.")

        if self.KEY_FILE not in self.app[self.OPENSSH_CONFIGURATION]:
            raise ScpException("Key file is required for scp.")

    def has_app(self):
        """
        Check if app was initialized
        :return: boolean
        """
        if self.app is None:
            return False

        return True

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
