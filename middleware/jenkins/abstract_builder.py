__author__ = 'aguimaraesviana'

from middleware.jenkins.parser.interface_parser import InterfaceParser
from middleware.gitlab.download import Download


class AbstractBuilder:
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
