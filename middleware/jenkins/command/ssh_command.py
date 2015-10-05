from middleware.openssh.ssh import Ssh


class SshCommand(object):

    def __init__(self, app, ssh=Ssh()):
        self.app = app
        self.ssh = ssh

    def execute(self, host, command):
        self.ssh.init_app(self.app)
        self.ssh.execute(host, command)
