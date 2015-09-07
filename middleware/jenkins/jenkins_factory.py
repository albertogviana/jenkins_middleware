from jenkins import Jenkins


class JenkinsFactory(object):
    @staticmethod
    def create(host, user=None, password=None):
        """
        Create a Jenkins instance
        :param host: ``str``
        :param user: ``str``
        :param password: ``str``
        :return: ``jenkins.Jenkins`` instance
        """
        server = Jenkins(host, user, password)
        return server
