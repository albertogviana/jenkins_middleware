from urllib.parse import urlparse

from .exceptions import OpensshException


class AbstractOpenSSH(object):
    OPENSSH_CONFIGURATION = "OPENSSH_CONFIGURATION"
    KEY_FILE = "key_file"
    USER = "user"

    app = None

    def has_app(self):
        """
        Check if app was initialized
        :return: boolean
        """
        if self.app is None:
            return False

        return True

    def init_app(self, app):
        """
        Initialize the class configuration
        :param app:
        :return:
        """
        if app is None:
            return

        self.app = app

        if self.OPENSSH_CONFIGURATION not in self.app:
            raise OpensshException("The OPENSSH_CONFIGURATION parameter was not found, it is required for openssh.")

        if self.USER not in self.app[self.OPENSSH_CONFIGURATION]:
            raise OpensshException("User parameter is required for openssh.")

        if self.KEY_FILE not in self.app[self.OPENSSH_CONFIGURATION]:
            raise OpensshException("Key file is required for openssh.")

    @classmethod
    def _get_host(cls, host):
        hostname = urlparse(host)

        if hostname.netloc is "":
            raise OpensshException("The host " + host + " informed is not valid for openssh.")

        return hostname.netloc
