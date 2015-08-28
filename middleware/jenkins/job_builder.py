from middleware.jenkins.parser.interface_parser import InterfaceParser
from middleware.jenkins.abstract_builder import AbstractBuilder
from os import path
import jenkins


class JobBuilder(AbstractBuilder):
    def create(self, job: InterfaceParser, jenkins_url):
        self._parser = job
        file = self.get_git_abstract_project(job)
        print(file)
        folder = self.extract_package(file)
        print(folder)
        self.pre_process_configuration(folder)

        try:
            server = jenkins.Jenkins(jenkins_url)
            r = server.create_job(self._parser.get_name(), path.join(folder, self.CONFIG_XML_PROCESSED))
            print(r)
        except Exception as inst:
            raise Exception(inst.args)

