from middleware.jenkins.parser.interface_parser import InterfaceParser
from middleware.jenkins.abstract_builder import AbstractBuilder
from os import path
from middleware.jenkins.jenkins_factory import JenkinsFactory


class JobBuilder(AbstractBuilder):
    def create(self, job: InterfaceParser, user, host, token):
        self._parser = job
        file = self.get_git_abstract_project(job)
        print(file)
        folder = self.extract_package(file)
        print(folder)
        self.pre_process_configuration(folder)

        try:
            server = JenkinsFactory().create(host,user,token)

            config_xml = self.get_file_content(path.join(folder, self.CONFIG_XML_PROCESSED))
            server.create_job(self._parser.get_name(), config_xml)
        except Exception as inst:
            raise Exception(inst.args)

