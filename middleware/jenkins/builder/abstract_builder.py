from subprocess import Popen, PIPE
from json.encoder import JSONEncoder
from os import path
from .interfaces import AbstractBuilderInterface
from middleware.jenkins.parser.interfaces import InterfaceParser
from .interfaces import BuilderInterface
from middleware.gitlab.download import Download
import tarfile


class AbstractBuilder(AbstractBuilderInterface, BuilderInterface):
    """
    Abstract Builder implements methods that it will be used for the concrete class
    """

    FOLDER_EXTENSION = '.git'
    CONFIG_XML_IN = 'config.xml'
    CONFIG_XML_PROCESSED = 'output.xml'

    """
    :param InterfaceParser
    """
    _parser = None

    def __init__(self, job: InterfaceParser, download: Download):
        self._parser = job
        self._download = download
        self.file = ''
        self.folder = ''
        self.config_xml = ''

    def get_git_abstract_project(self, parser: InterfaceParser):
        """
        Get the archieve on gitlab
        :param parser: InterfaceParser
        :return: file path
        """
        file = self._download.get_archieve(
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
        except Exception as inst:
            raise Exception(inst)
        finally:
            tar.close()

        return path.join(directory, self._parser.get_abstract_name() + self.FOLDER_EXTENSION)

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
            raise Exception(output)

    @classmethod
    def get_file_content(cls, file):
        """
        Return the file content
        :param file: string
        :return: string
        """

        if not path.isfile(file):
            raise Exception("File %s was not found" % file)

        handle = open(file)
        try:
            content = handle.read()
        except Exception as inst:
            raise Exception(inst)
        finally:
            handle.close()

        return content

    def process(self):
        """
        Process the abstract job
        :return:
        """
        try:
            self.file = self.get_git_abstract_project(self._parser)
            self.folder = self.extract_package(self.file)
            self.pre_process_configuration(self.folder)
            self.config_xml = self.get_file_content(path.join(self.folder, self.CONFIG_XML_PROCESSED))
        except Exception as inst:
            raise Exception(inst.args)

    def get_name(self):
        """
        Get job name
        :return: string
        """
        return self._parser.get_name()

    def get_config_xml(self):
        """
        Get config.xml
        :return: string
        """
        return self.config_xml

    def get_folder(self):
        return self.folder
