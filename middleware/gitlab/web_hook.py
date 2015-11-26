import re

from .parser import Parser
from middleware.jenkins.util import get_application_configuration
from middleware.jenkins.jenkins_api import JenkinsApi
from werkzeug.exceptions import UnprocessableEntity, Forbidden


class WebHook(object):

    branch_pattern = {
        "master": "master",
        "develop": "develop",
        "feature": "feature[-/]{1}",
        "release": "(hotfix|release)[-/]{1}"
    }

    def __init__(self, app, logger):
        self.app_configuration = app
        self.logger = logger
        self.jenkins_server = None

    def push(self, json_data):
        """
        Trigger pipeline
        :param json_data:
        :return:
        """
        self.logger.info(json_data)

        if "total_commits_count" in json_data and json_data["total_commits_count"] == 0:
            raise Forbidden(description=str("No commit found"))

        try:
            parser = Parser(json_data)
            repository_namespace = parser.get_repository_namespace()
            repository_project_name = parser.get_project_name()
            branch_name = parser.get_branch_name()

            pipeline_type = self.get_pipeline_type(branch_name)

            configuration = self.get_jenkins_configuration(repository_namespace)

            user = self.app_configuration["JENKINS_USER"]
            self.jenkins_server = self.get_jenkins_instance(
                configuration.host, user, configuration.token
            )

            job_name = self.get_job_name(repository_namespace, repository_project_name, pipeline_type)
            parameters = {"branchName": branch_name}
            self.jenkins_server.run_job(job_name, configuration.token, parameters)

            return ''
        except Exception as inst:
            self.logger.error(inst)
            raise UnprocessableEntity(description=str(inst))

    def get_job_name(self, repository_namespace, repository_project_name, pipeline_type):
        """
        Verify the pipeline name if it is using the short or long name
        :param repository_namespace: str
        :param repository_project_name: str
        :param pipeline_type: str
        :return: str
        """
        test_job_name_pattern2 = repository_project_name + '-' + pipeline_type + '-start'
        if self.jenkins_server.job_exists(test_job_name_pattern2) is True:
            return test_job_name_pattern2

        test_job_name_pattern = repository_namespace + '-' + repository_project_name + '-' + pipeline_type + '-pipeline-start'
        if self.jenkins_server.job_exists(test_job_name_pattern) is True:
            return test_job_name_pattern

        raise Exception("The start job for $repositoryProjectName doesn't exists.")

    def get_pipeline_type(self, branch_name):
        """
        Verify what is the pipeline type
        :param branch_name: str
        :return:
        """
        for key in self.branch_pattern:
            if re.match(self.branch_pattern[key], branch_name) is not None:
                return key

        raise Exception("The branch %s is not follow the name convention." % branch_name)

    @classmethod
    def get_jenkins_configuration(cls, team_name):
        return get_application_configuration(team_name)

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
