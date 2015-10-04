import os
from middleware.openssh.scp import Scp
from middleware.jenkins.builder.interface.builder_executor import BuilderExecutor
from middleware.jenkins.jenkins_api import JenkinsApi
from middleware.jenkins.command.ssh_command import SshCommand


class ScpCommand(object):
    folders_to_move = ['assets']
    files_to_move = ['build.xml']

    COMMAND = r'"bash -c \"if [ ! -d {jenkins}/{folder} ]; then  mkdir -p {jenkins}/{folder}; fi\""'

    def __init__(self, app_configuration, jenkins_api: JenkinsApi):
        self.app_configuration = app_configuration
        self.jenkins_api = jenkins_api
        self.scp = self.get_scp_instance()

    def execute(self, item: BuilderExecutor, server):
        jenkins_folder = self.jenkins_api.get_jenkins_home()
        ggs_job_folder = 'ggs-jobs/' + item.get_name()
        command = self.COMMAND.format(jenkins=jenkins_folder, folder=ggs_job_folder)

        ssh = self.get_ssh_command_instance()
        ssh.execute(self.jenkins_api.server, command)

        for folder in self.folders_to_move:
            if os.path.isdir(os.path.join(item.get_folder(), folder)) is True:
                self.scp.execute(
                    os.path.join(item.get_folder(), folder),
                    jenkins_folder + '/ggs-jobs/' + item.get_name(),
                    server
                )

        for file in self.files_to_move:
            if os.path.isfile(os.path.join(item.get_folder(), file)) is True:
                self.scp.execute(
                    os.path.join(item.get_folder(), file),
                    jenkins_folder + '/ggs-jobs/' + item.get_name(),
                    server
                )

    def get_scp_instance(self):
        return Scp(self.app_configuration["OPENSSH_CONFIGURATION"])

    def get_ssh_command_instance(self):
        return SshCommand(self.app_configuration)
