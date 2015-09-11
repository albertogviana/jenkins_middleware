from middleware.jenkins.parser.parser import Parser
from middleware.jenkins.job_builder import JobBuilder
from middleware.jenkins.model.configuration import Configuration as ConfigurationModel
from middleware import configuration


class JenkinsFacade(object):
    def create(self, json_data):
        user = configuration.get('jenkins', 'user')
        jenkins_configuration = self.get_application_configuration(json_data["namespace"])

        if 'jobs' in json_data:
            self.__job_builder(json_data, user, jenkins_configuration.host, jenkins_configuration.token)
        return json_data

    @classmethod
    def __job_builder(cls, jobs_data, user, host, token):
        for job_data in jobs_data['jobs']:
            job_parser = Parser(job_data)
            JobBuilder().create(job_parser, user, host, token)

        return True

    @classmethod
    def get_application_configuration(cls, team_name):
        try:
            return ConfigurationModel.query.filter_by(team_name=team_name).one()
        except Exception as inst:
            if type(inst).__name__ == "NoResultFound":
                raise Exception('No configuration found for team %s jenkins. Please add it.' % team_name)

            raise Exception(str(inst))
