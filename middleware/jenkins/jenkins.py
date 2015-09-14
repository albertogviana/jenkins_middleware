from jenkins import Jenkins as PythonJenkins


class Jenkins(PythonJenkins):
    def __int__(self, host, user=None, password=None):
        """
        Create a Jenkins instance
        :param host: ``str``
        :param user: ``str``
        :param password: ``str``
        :return: ``jenkins.Jenkins`` instance
        """
        super().__init__.__init__(host, user, password)
