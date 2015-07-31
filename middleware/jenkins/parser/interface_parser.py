__author__ = 'aguimaraesviana'


class InterfaceParser:
    def get_placeholder(self, placeholder_name):
        raise NotImplementedError()

    def get_job_parameter(self, job_parameter_name):
        raise NotImplementedError()

    def get_name(self):
        raise NotImplementedError()

    def get_abstract_name(self):
        raise NotImplementedError()

    def get_abstract_version(self):
        raise NotImplementedError()
