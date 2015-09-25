from middleware.jenkins.parser.interface.parser import InterfaceParser


class Builder(object):
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
