import time

import requests
import tempfile
import os
from middleware.gitlab.interface.gitlab import InterfaceGitlab


class Download(InterfaceGitlab):
    """
    Get files from gitlab
    """

    FILE_EXTENSION = '.tar.gz'

    """
    Gitlab parameters
    """
    HOST = 'host'
    DOWNLOAD_PATH = 'download_path'
    TAG_PATH = 'tag_path'
    PRIVATE_TOKEN = 'private_token'

    def __init__(self, configuration: dict):
        self.configuration = configuration

    def __get_configuration(self, key):
        """
        Get configuration
        :param key: string
        :return: string
        """
        if key not in self.configuration:
            raise Exception("It was not possible to find the gitlab key " + key + " in configuration.")

        return self.configuration[key]

    def get_archieve(self, job_name, abstract_name, version):
        """
        Get the archieve on gitlab
        :param job_name:
        :param abstract_name:
        :param version:
        :return: the path and file
        """

        if version.endswith('*'):
            version = self.get_latest_version(abstract_name, version)

        host = self.__get_configuration(self.HOST) + '/' + self.__get_configuration(self.DOWNLOAD_PATH)
        host = host.format(*[abstract_name, version])

        abstract_job_file = self.__prepare_file(job_name, abstract_name)

        response = requests.get(host, stream=True)

        if response.status_code != 200:
            raise Exception(
                "It was not find the abstract job " + abstract_name + " in gitlab."
            )

        with open(abstract_job_file, 'wb') as handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    handle.write(chunk)
                    handle.flush()

        return abstract_job_file

    def __prepare_file(self, job_name, abstract_name):
        """
        Create a directory and prepare file
        :param job_name: job name
        :param abstract_name: abstract name
        :return: the directory path and the filename
        """
        directory = os.path.join(tempfile.gettempdir(), job_name) + '%s' % time.time()

        if os.path.exists(directory) is False:
            os.mkdir(directory)

        return os.path.join(directory, abstract_name + self.FILE_EXTENSION)

    def get_latest_version(self, abstract_name, version):
        """
        Get latest version on gitlab
        :param abstract_name: string
        :param version: string
        :return: string
        """
        host = self.__get_configuration(self.HOST) + '/' + self.__get_configuration(self.TAG_PATH)
        private_token = self.__get_configuration(self.PRIVATE_TOKEN)
        host = host.format(*[abstract_name, private_token])

        response = requests.get(host)

        if response.status_code != 200:
            raise Exception("It was not possible to get the tags for abstract job " + abstract_name + " in gitlab.")

        if version.endswith('*'):
            version_prefix = version[:-1]

        tags = response.json()
        for tag in tags:
            if tag["name"].find(version_prefix) != -1:
                return tag["name"]

        raise Exception("No matching version for " + abstract_name + " " + version + ".")
