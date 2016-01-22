import ssl
import socket

from jenkins import Jenkins as PythonJenkins
from jenkins import JenkinsException
from six.moves.urllib.request import HTTPSHandler, install_opener, build_opener


class JenkinsApi(PythonJenkins):
    """
    Class to handle Jenkins integration
    """

    def __init__(self, url, username=None, password=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        super().__init__(url, username, password, timeout)

        # Setting ssl key verificationas false
        context = ssl._create_stdlib_context(check_hostname=False)
        unverified_handler = HTTPSHandler(context=context, check_hostname=False)
        install_opener(build_opener(unverified_handler))

    def handle_job(self, name, config_xml):
        if self.job_exists(name) is True:
            self.reconfig_job(name, config_xml)
        else:
            self.create_job(name, config_xml)

    def handle_view(self, name, config_xml):
        if self.view_exists(name) is True:
            self.reconfig_view(name, config_xml)
        else:
            self.create_view(name, config_xml)

    def get_jenkins_home(self, node="(master)"):
        response = self.get_node_info(node)

        if "path" not in response["monitorData"]["hudson.node_monitors.DiskSpaceMonitor"]:
            raise JenkinsException(
                "It was not possible to find the jenkins home. Please check your jenkins " + self.server
            )

        return response["monitorData"]["hudson.node_monitors.DiskSpaceMonitor"]["path"]

    def run_job(self, name, token=None, parameters=None):
        if self.job_exists(name) is True:
            self.build_job(name, token=token, parameters=parameters)
