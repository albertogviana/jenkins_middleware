from middleware.jenkins.parser.parser import Parser
from middleware.jenkins.job_builder import JobBuilder
import jenkins


class JenkinsFacade:

    def create(self, json_data):
        if 'jenkins_url' not in json_data:
            raise Exception('Inform Jenkins url')

        jenkins_url = json_data['jenkins_url']
        #
        # server = jenkins.Jenkins(jenkins_url)
        # version = server.get_version()
        # print(version)

        if 'jobs' in json_data:
            self.__job_builder(json_data, jenkins_url)
        return json_data

    def __job_builder(self, jobs_data, jenkins_url):
        for job_data in jobs_data['jobs']:
            job_parser = Parser(job_data)
            JobBuilder().create(job_parser, jenkins_url)

        return True

