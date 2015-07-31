__author__ = 'aguimaraesviana'

from middleware.jenkins.parser.parser import Parser
from middleware.jenkins.job_builder import JobBuilder

class JenkinsFacade:

    def create(self, json_data):
        if 'jobs' in json_data:
            self.__job_builder(json_data)
        return json_data

    def __job_builder(self, jobs_data):
        for job_data in jobs_data['jobs']:
            job_parser = Parser(job_data)
            JobBuilder().create(job_parser)

        return True
