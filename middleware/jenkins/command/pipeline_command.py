from middleware.jenkins.jenkins_api import JenkinsApi
from ..builder.pipeline import Pipeline
from middleware.jenkins.command.scp_command import ScpCommand


class PipelineCommand(object):
    def __init__(self, app, jenkins_api: JenkinsApi, scp_command=ScpCommand()):
        self.app = app
        self.jenkins_api = jenkins_api
        self.scp_command = scp_command
        self.scp_command.init_app(self.app)

    def execute(self, pipeline: Pipeline):
        self._handle_job(pipeline)
        self._handle_view(pipeline)

    def _handle_job(self, pipeline: Pipeline):
        """
        Create/Update a job on jenkins
        :param pipeline:
        :return:
        """
        for item in pipeline.jobs:
            self.jenkins_api.handle_job(item.get_name(), item.get_config_xml())
            self.scp_command.execute(item, self.jenkins_api, self.jenkins_api.server)

    def _handle_view(self, pipeline: Pipeline):
        """
        Handle the view creation
        :param pipeline:
        :return:
        """
        for item in pipeline.views:
            self.jenkins_api.handle_view(item.get_name(), item.get_config_xml())
            self.scp_command.execute(item, self.jenkins_api, self.jenkins_api.server)
