import os
from middleware.openssh.scp import Scp
from middleware.openssh.ssh import Ssh
from ..builder.interfaces import BuilderInterface


class ScpCommand(object):
    GGS_JOBS_FOLDER = 'ggs-jobs'

    folders_to_move = ['assets']
    files_to_move = ['build.xml']

    SSH_COMMAND = r'"bash -c \"if [ ! -d {jenkins}/{folder} ]; then  mkdir -p {jenkins}/{folder}; fi\""'

    def __init__(self, app=None, ssh=Ssh(), scp=Scp()):
        self.app = None
        self.ssh = ssh
        self.scp = scp

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.ssh.init_app(self.app)
        self.scp.init_app(self.app)

    def execute(self, item: BuilderInterface, jenkins_api, server):
        """
        Move files to jenkins server
        :param item:
        :param jenkins_api:
        :param server:
        :return:
        """
        jenkins_folder = jenkins_api.get_jenkins_home()
        ggs_job_folder = self.GGS_JOBS_FOLDER + '/' + item.get_name()
        command = self.SSH_COMMAND.format(jenkins=jenkins_folder, folder=ggs_job_folder)

        self.ssh.execute(jenkins_api.server, command)

        for folder in self.folders_to_move:
            if os.path.isdir(os.path.join(item.get_folder(), folder)) is True:
                self.scp.execute(
                    os.path.join(item.get_folder(), folder),
                    jenkins_folder + '/' + self.GGS_JOBS_FOLDER + '/' + item.get_name(),
                    server
                )

        for file in self.files_to_move:
            if os.path.isfile(os.path.join(item.get_folder(), file)) is True:
                self.scp.execute(
                    os.path.join(item.get_folder(), file),
                    jenkins_folder + '/' + self.GGS_JOBS_FOLDER + '/' + item.get_name(),
                    server
                )

