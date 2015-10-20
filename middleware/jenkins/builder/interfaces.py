from middleware.jenkins.parser.interfaces import InterfaceParser


class AbstractBuilderInterface(object):
    def get_git_abstract_project(self, parser: InterfaceParser):
        """
        Get the archieve on gitlab
        :param parser: InterfaceParser
        :return: file path
        """
        raise NotImplementedError()

    def pre_process_configuration(self, directory):
        """
        Pre process the configuration
        :param directory: string
        """
        raise NotImplementedError()

    def extract_package(self, compress_file):
        """
        Extract the tar.gz file and return the path
        :param compress_file:
        :return: folder path
        """
        raise NotImplementedError()

    @classmethod
    def get_file_content(cls, file):
        """
        Return the file content
        :param file: string
        :return: string
        """
        raise NotImplementedError()


class BuilderInterface(object):
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
