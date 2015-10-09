from middleware.jenkins.parser.parser import Parser
from middleware.jenkins.builder.job_builder import JobBuilder
from middleware.jenkins.builder.view_builder import ViewBuilder
from middleware.jenkins.models import Configuration as ConfigurationModel
from middleware.jenkins.builder.pipeline import Pipeline
from middleware.gitlab.download import Download
from .jenkins_api import JenkinsApi
from sqlalchemy.orm.exc import NoResultFound
from middleware.jenkins.command.pipeline_command import PipelineCommand
from werkzeug.exceptions import BadRequest, UnprocessableEntity


class Facade(object):
    """
    Jenkins Facade
    """

    SYNC_JOBS_ASSETS_TO_SLAVE = "sync-jobsassets-to-slave"

    def __init__(self, app, pipeline=None):
        self.app_configuration = app
        self.jenkins_configuration = None

        if pipeline is None:
            pipeline = Pipeline()

        self.pipeline = pipeline

    def process(self, json_data):
        """
        Create job and views
        :param json_data: str
        :return:
        """
        try:
            if json_data is None or len(json_data) == 0:
                raise BadRequest(description="Invalid json.")

            self.jenkins_configuration = self.get_application_configuration(json_data["namespace"])

            if 'jobs' in json_data:
                self.__job_builder(json_data)

            if 'view' in json_data:
                self.__view_builder(json_data)

            self.execute()

            return ''
        except Exception as inst:
            raise UnprocessableEntity(description=str(inst))

    def __job_builder(self, jobs_data):
        """
        Create job
        :param jobs_data:
        :param pipeline:
        :return:
        """
        download = self.get_download_instance()
        for job_data in jobs_data['jobs']:
            job_parser = Parser(job_data)
            job = JobBuilder(job_parser, download)
            job.process()
            self.pipeline.add_job(job)

    def __view_builder(self, view_data):
        """
        Create job
        :param view:
        :param pipeline:
        :return:
        """
        download = self.get_download_instance()
        view_parser = Parser(view_data['view'])
        view = ViewBuilder(view_parser, download)
        view.process()
        self.pipeline.add_view(view)

    def execute(self):
        user = self.app_configuration["JENKINS_USER"]
        jenkins_server = self.get_jenkins_instance(
            self.jenkins_configuration.host, user, self.jenkins_configuration.token
        )
        pipeline_command = PipelineCommand(self.app_configuration, jenkins_server)
        pipeline_command.execute(self.pipeline)

        jenkins_server.run_job(self.SYNC_JOBS_ASSETS_TO_SLAVE, self.jenkins_configuration.token)

    @classmethod
    def get_application_configuration(cls, team_name):
        """
        Return a configuration object with jenkins configuration
        :param team_name: string
        :return: ConfigurationModel
        """
        try:
            return ConfigurationModel.query.filter_by(team_name=team_name).one()
        except NoResultFound:
            raise Exception('No configuration found for team %s. Please add it.' % team_name)
        except Exception as inst:
            raise Exception(str(inst))

    @classmethod
    def get_jenkins_instance(cls, host, user, password):
        """
        Get jenkins instance
        :param host: string
        :param user: string
        :param password: string
        :return: Jenkins
        """
        return JenkinsApi(host, user, password)

    def get_download_instance(self):
        """
        Get jenkins instance
        :param host: string
        :param user: string
        :param password: string
        :return: Jenkins
        """
        return Download(self.app_configuration["GITLAB_CONFIGURATION"])
