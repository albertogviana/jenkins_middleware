from middleware.jenkins.builder.abstract_builder import AbstractBuilder
from os import path


class JobBuilder(AbstractBuilder):
    """
    Job Builder
    """

    def create(self):
        """
        Create job on jenkins
        :return:
        """
        try:
            file = self.get_git_abstract_project(self._parser)
            folder = self.extract_package(file)
            self.pre_process_configuration(folder)

            config_xml = self.get_file_content(path.join(folder, self.CONFIG_XML_PROCESSED))
            self._jenkins.create_job(self._parser.get_name(), config_xml)
        except Exception as inst:
            raise Exception(inst.args)
