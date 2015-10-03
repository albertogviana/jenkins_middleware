from middleware.jenkins.parser.parser import Parser
from middleware.jenkins.builder.job_builder import JobBuilder
from middleware.jenkins.models import Configuration as ConfigurationModel
from middleware.jenkins.builder.pipeline import Pipeline
from middleware.gitlab.download import Download
from middleware.jenkins.services.jenkins_api import JenkinsApi
from sqlalchemy.orm.exc import NoResultFound
from middleware.jenkins.command.pipeline_command import PipelineCommand
from ..exceptions import ValidationError
from werkzeug.exceptions import BadRequest


class Facade(object):
    """
    Jenkins Facade
    """

    def __init__(self, app_configuration):
        self.app_configuration = app_configuration
        self.jenkins_configuration = None
        self.pipeline = Pipeline()

    def process(self, json_data):
        """
        Create job and views
        :param json_data:
        :return:
        """

        if json_data is None:
            #{'status': 400, 'error': 'bad request', 'message': "Invalid json."}
            print("Exception")
            raise Exception("Invalid json.")

        print(json_data)
        self.jenkins_configuration = self.get_application_configuration(json_data["namespace"])

        if 'jobs' in json_data:
            self.__job_builder(json_data)

        self.execute()

        return json_data

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

    def execute(self):
        user = self.app_configuration["JENKINS_USER"]
        jenkins_server = self.get_jenkins_instance(
            self.jenkins_configuration.host, user, self.jenkins_configuration.token
        )
        pipeline_command = PipelineCommand(self.app_configuration, jenkins_server)
        pipeline_command.execute(self.pipeline)

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
            raise Exception('No configuration found for team %s jenkins. Please add it.' % team_name)
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
