from middleware.jenkins.parser.interface.interface_parser import InterfaceParser


class Parser(InterfaceParser):
    """
    Json parser
    """
    JOB_KEY = 'job'
    JOB_NOT_FOUND = 'Job field was not found.'

    PLACEHOLDER_KEY = 'placeholder'
    PLACEHOLDER_NOT_FOUND = 'Placeholder field was not found.'

    # json data with job parameters
    __json_data = {}

    def __init__(self, json_data):
        self.__json_data = json_data

    def get_json_data(self):
        """
        Get the complete json
        :return:
        """
        return self.__json_data

    def _has_job(self):
        """
        Check if the field job exists
        :return: boolean
        """
        if self.JOB_KEY in self.__json_data:
            return True
        return False

    def get_job_parameter(self, job_parameter_name):
        """
        Get a field
        :param job_parameter_name: string
        :return: string
        """
        if self._has_job() is False:
            raise Exception(self.JOB_NOT_FOUND)

        if job_parameter_name not in self.__json_data[self.JOB_KEY]:
            raise Exception(job_parameter_name + " field was not found.")

        return self.__json_data[self.JOB_KEY][job_parameter_name]

    def get_name(self):
        """
        Get name
        :return: string
        """
        return self.get_job_parameter('name')

    def get_abstract_name(self):
        """
        Get abstract name
        :return: string
        """
        return self.get_job_parameter('abstract_name')

    def get_abstract_version(self):
        """
        Get abstract version
        :return: string
        """
        return self.get_job_parameter('version')

    def _has_placeholder(self):
        """
        Check if the field job exists
        :return: boolean
        """
        if self.PLACEHOLDER_KEY in self.__json_data:
            return True
        return False

    def get_placeholder(self, placeholder_name):
        """
        Get a placeholder
        :param placeholder_name:
        :return: string
        """
        if self._has_placeholder() is False:
            raise Exception(self.PLACEHOLDER_NOT_FOUND)

        if placeholder_name not in self.__json_data[self.PLACEHOLDER_KEY]:
            raise Exception(placeholder_name + " field was not found.")

        return self.__json_data[self.PLACEHOLDER_KEY][placeholder_name]

    def get_placeholders(self):
        """
        Get all placeholders
        :return: dict
        """
        if self._has_placeholder() is False:
            raise Exception(self.PLACEHOLDER_NOT_FOUND)

        return self.__json_data[self.PLACEHOLDER_KEY]
