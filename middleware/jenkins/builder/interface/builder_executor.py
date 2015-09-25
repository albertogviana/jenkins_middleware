class BuilderExecutor(object):
    def process(self):
        """
        Process the abstract job
        :return:
        """
        raise NotImplementedError()

    def get_name(self):
        """
        Get job name
        :return: string
        """
        raise NotImplementedError()

    def get_config_xml(self):
        """
        Get the config.xml
        :return: string
        """
        raise NotImplementedError()

    def get_folder(self):
        """
        Get folder
        :return: string
        """
        raise NotImplementedError()

