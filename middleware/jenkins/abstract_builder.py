from middleware.jenkins.parser.interface_parser import InterfaceParser
from middleware.gitlab.download import Download
from os import path
from subprocess import Popen, PIPE
import tarfile
from json.encoder import JSONEncoder


class AbstractBuilder(object):

    FOLDER_EXTENSION = '.git'
    CONFIG_XML_IN = 'config.xml'
    CONFIG_XML_PROCESSED = 'output.xml'

    """
    :param InterfaceParser
    """
    _parser = None

    _jenkins = None

    _user = ''

    @classmethod
    def get_git_abstract_project(cls, parser: InterfaceParser):
        """
        Get the archieve on gitlab
        :param parser: InterfaceParser
        :return: file path
        """
        file = Download().get_archieve(
            parser.get_name(),
            parser.get_abstract_name(),
            parser.get_abstract_version()
        )

        return file

    def extract_package(self, compress_file):
        """
        Extract the tar.gz file and return the path
        :param compress_file:
        :return: folder path
        """
        try:
            directory = path.dirname(compress_file)
            tar = tarfile.open(compress_file)
            tar.extractall(path=directory)
            tar.close()

            return path.join(directory, self._parser.get_abstract_name() + self.FOLDER_EXTENSION)
        except Exception as inst:
            raise Exception(inst)

    def pre_process_configuration(self, directory):
        """
        Pre process the configuration
        :param directory: string
        """
        placeholders = JSONEncoder().encode(self._parser.get_placeholders())
        config_xml = path.join(directory, self.CONFIG_XML_IN)
        output_xml = path.join(directory, self.CONFIG_XML_PROCESSED)
        command = "%s/replace '%s' %s %s" % (directory, placeholders, config_xml, output_xml)

        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        output = process.communicate()

        if process.returncode == 1:
            raise Exception(output.decode('utf-8'))

    @classmethod
    def get_file_content(cls, file):
        """
        Return the file content
        :param file: string
        :return: string
        """

        if not path.isfile(file):
            raise Exception("File %s not found" % file)

        handle = open(file)
        content = handle.read()
        handle.close()

        return content

