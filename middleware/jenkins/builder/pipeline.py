from .job_builder import JobBuilder
from .view_builder import ViewBuilder


class Pipeline(object):
    """
    Class handles Pipeline composition objects
    """

    def __init__(self):
        self.jobs = []
        self.views = []

    def add_job(self, job: JobBuilder):
        self.jobs.append(job)

    def add_view(self, view: ViewBuilder):
        self.views.append(view)
