from middleware.jenkins.services.jenkins_api import JenkinsApi
from middleware.jenkins.builder.pipeline import Pipeline
from middleware.jenkins.command.scp_command import ScpCommand


class PipelineCommand(object):
    def __init__(self, app_configuration, jenkins_api: JenkinsApi):
        self.app_configuration = app_configuration
        self.jenkins_api = jenkins_api
        self.scp = self.get_scp_command_instance()

    def execute(self, pipeline: Pipeline):
        self._handle_job(pipeline)

    def _handle_job(self, pipeline: Pipeline):
        for item in pipeline.jobs:
            self.jenkins_api.handle_job(item.get_name(), item.get_config_xml())
            self.scp.execute(item, self.jenkins_api.server)

    def get_scp_command_instance(self):
        return ScpCommand(self.app_configuration, self.jenkins_api)
