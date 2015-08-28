__author__ = 'aguimaraesviana'

from middleware.jenkins.parser.interface_parser import InterfaceParser
from middleware.jenkins.abstract_builder import AbstractBuilder


class JobBuilder(AbstractBuilder):
    def create(self, job: InterfaceParser):
        self._parser = job
        file = self.get_git_abstract_project(job)
        print(file)
        folder = self.extract_package(file)
        print(folder)
