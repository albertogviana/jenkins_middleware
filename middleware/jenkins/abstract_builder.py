__author__ = 'aguimaraesviana'

from middleware.jenkins.parser.interface_parser import InterfaceParser
from middleware.gitlab.download import Download
import tarfile
from os import path


class AbstractBuilder:

    FOLDER_EXTENSION = '.git'

    '''
    :param InterfaceParser
    '''
    _parser = ''

    def get_git_abstract_project(self, parser: InterfaceParser):
        '''
        Get the archieve on gitlab
        :param parser: InterfaceParser
        :return: file path
        '''
        file = Download().get_archieve(
            parser.get_name(),
            parser.get_abstract_name(),
            parser.get_abstract_version()
        )

        return file

    def extract_package(self, compress_file):
        '''
        Extract the tar.gz file and return the path
        :param compress_file:
        :return string:folder path
        '''
        try:
            directory = path.dirname(compress_file)
            tar = tarfile.open(compress_file)
            tar.extractall(path=directory)
            tar.close()

            return path.join(directory, self._parser.get_abstract_name() + self.FOLDER_EXTENSION)
        except Exception as inst:
            raise Exception(inst)

