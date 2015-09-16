from middleware.jenkins.parser.parser import Parser
from middleware.jenkins.job_builder import JobBuilder
from middleware.jenkins.model.configuration import Configuration as ConfigurationModel
from middleware import configuration
from middleware.jenkins.jenkins import Jenkins


class JenkinsFacade(object):
    """
    Jenkins Facade
    """
    def create(self, json_data):
        """
        Create job and views
        :param json_data:
        :return:
        """
        user = configuration.get('jenkins', 'user')
        jenkins_configuration = self.get_application_configuration(json_data["namespace"])

        jenkins_server = self.get_jenkins_instance(jenkins_configuration.host, user, jenkins_configuration.token)

        if 'jobs' in json_data:
            self.__job_builder(json_data, jenkins_server)
        return json_data

    @classmethod
    def __job_builder(cls, jobs_data, jenkins_server):
        """
        Create job
        :param jobs_data:
        :param jenkins_server:
        :return:
        """
        for job_data in jobs_data['jobs']:
            job_parser = Parser(job_data)
            JobBuilder(job_parser, jenkins_server)

        return True

    @classmethod
    def get_application_configuration(cls, team_name):
        """
        Return a configuration object with jenkins configuration
        :param team_name: string
        :return: ConfigurationModel
        """
        try:
            return ConfigurationModel.query.filter_by(team_name=team_name).one()
        except Exception as inst:
            if type(inst).__name__ == "NoResultFound":
                raise Exception('No configuration found for team %s jenkins. Please add it.' % team_name)

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
        return Jenkins(host, user, password)
