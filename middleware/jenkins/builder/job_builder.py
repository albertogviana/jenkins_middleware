from middleware.jenkins.builder.abstract_builder import AbstractBuilder
from middleware.jenkins.builder.interface.builder_executor import BuilderExecutor
from os import path


class JobBuilder(AbstractBuilder, BuilderExecutor):
    """
    Job Builder
    """
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
