class InterfaceParser(object):
    """
    Interface for parser
    """

    def get_placeholder(self, placeholder_name):
        """
        Get a placeholder
        :param placeholder_name:
        :return: string
        """
        raise NotImplementedError()

    def get_placeholders(self):
        """
        Get all placeholders
        :return: dict
        """
        raise NotImplementedError()

    def get_job_parameter(self, job_parameter_name):
        """
        Get a field
        :param job_parameter_name: string
        :return: string
        """
        raise NotImplementedError()

    def get_name(self):
        """
        Get name
        :return: string
        """
        raise NotImplementedError()

    def get_abstract_name(self):
        """
        Get abstract name
        :return: string
        """
        raise NotImplementedError()

    def get_abstract_version(self):
        """
        Get abstract version
        :return: string
        """
        raise NotImplementedError()
