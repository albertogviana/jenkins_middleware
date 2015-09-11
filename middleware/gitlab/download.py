import time

from middleware import configuration
import requests
import tempfile
import os


class Download(object):
    """
    Get files from gitlab
    """

    FILE_EXTENSION = '.tar.gz'

    def get_archieve(self, job_name, abstract_name, version):
        """
        Get the archieve on gitlab
        :param job_name:
        :param abstract_name:
        :param version:
        :return: the path and file
        """

        if version.endswith('*'):
            latest_version = self.get_latest_version(abstract_name)
            if latest_version is not None:
                version = latest_version

        host = configuration.get('gitlab', 'host') + '/' + configuration.get('gitlab', 'download_path')
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

    @classmethod
    def get_latest_version(cls, abstract_name):
        """
        Get latest version on gitlab
        :param abstract_name: string
        :return: string
        """
        host = configuration.get('gitlab', 'host', raw=True) + '/' + \
               configuration.get('gitlab', 'tag_path', raw=True)
        private_token = configuration.get('gitlab', 'private_token', raw=True)
        host = host.format(*[abstract_name, private_token])

        response = requests.get(host)

        if response.status_code != 200:
            raise Exception(
                "It was not possible to get the tags for abstract job " + abstract_name + " in gitlab.")

        result = response.json()
        # Get the first element
        first_element = result.pop(0)
        if 'name' not in first_element:
            return None

        return first_element["name"]
