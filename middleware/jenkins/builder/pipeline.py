from middleware.jenkins.builder.job_builder import JobBuilder


class Pipeline(object):
    def __init__(self):
        self.jobs = []
        self.views = []

    def add_job(self, job: JobBuilder):
        self.jobs.append(job)
