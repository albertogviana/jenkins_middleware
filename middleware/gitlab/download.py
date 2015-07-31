__author__ = 'aguimaraesviana'

from middleware import configuration
import requests
import tempfile
import time
import os


class Download:
    FILE_EXTENSION = '.tar.gz'

    def get_archieve(self, job_name, abstract_name, version):
        '''
        Get the archieve on gitlab
        :param job_name:
        :param abstract_name:
        :param version:
        :return: the path and file
        '''
        host = configuration.get('gitlab', 'host') + '/' + configuration.get('gitlab', 'download_path')
        host = host.format(*[abstract_name, version])

        file = self.__prepare_file(job_name, abstract_name)

        response = requests.get(host, stream=True)

        if response.status_code != 200:
            raise Exception("It was not find the abstract job " + abstract_name + " in gitlab.")

        with open(file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()

        return file

    def __prepare_file(self, job_name, abstract_name):
        '''
        Create a directory and prepare file
        :param job_name: job name
        :param abstract_name: abstract name
        :return: the directory path and the filename
        '''
        directory = os.path.join(tempfile.gettempdir(), job_name) + '%s' % time.time()

        if os.path.exists(directory) is False:
            os.mkdir(directory)

        return os.path.join(directory, abstract_name + self.FILE_EXTENSION)
