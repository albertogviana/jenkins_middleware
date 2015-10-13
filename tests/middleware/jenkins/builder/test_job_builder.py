import time
import tempfile
import os
from middleware.jenkins.builder.job_builder import JobBuilder
from middleware.jenkins.parser.parser import Parser
from middleware.gitlab.download import Download
from unittest.mock import Mock
import pytest


class TestJobBuilder(object):
    FILENAME = "build-composer-cc2632fae2cab2f73ce6e6607d9b0befec0b82a1.tar.gz"

    directory = None

    def test_get_git_abstract_project(self):
        parser = Parser(self._get_parser_data())

        download = Download(self.get_git_download_data())
        download.get_archieve = Mock(
            return_value="/tmp/unitests/build-composer-cc2632fae2cab2f73ce6e6607d9b0befec0b82a1.tar.gz")
        job = JobBuilder(parser, download)
        file = job.get_git_abstract_project(parser)

        assert file is "/tmp/unitests/build-composer-cc2632fae2cab2f73ce6e6607d9b0befec0b82a1.tar.gz"

    def test_extract_package(self):
        parser = Parser(self._get_parser_data())
        download = Download(self.get_git_download_data())

        job = JobBuilder(parser, download)

        directory = self.prepare_fixture(parser.get_name(), parser.get_abstract_name())
        job.extract_package(os.path.join(directory, self.FILENAME))

        assert os.path.isdir(os.path.join(self.directory, parser.get_abstract_name() + ".git")) is True
        self.remove_fixture()

    @classmethod
    def _get_parser_data(cls):
        return {
            "format_version": "1.0",
            "job": {
                "name": "php-composer",
                "abstract_name": "build-composer",
                "version": "v*"
            },
            "placeholder": {
                "UPSTREAM_PROJECT": "my-upstream-project",
                "DOWNSTREAM_PROJECT": "my-downstream-project"
            }
        }

    @classmethod
    def get_git_download_data(cls):
        return {
            "host": "https://localhost",
            "tag_path": "api/v3/projects/web-jenkins-jobs%2F{}/repository/tags?private_token={}",
            "private_token": "123456",
            "download_path": "web-jenkins-jobs/{}/repository/archive.tar.gz?ref={}"
        }

    def prepare_fixture(self, job_name, abstract_name, file_extension=".git"):
        directory = os.path.join(tempfile.gettempdir(), job_name) + '%s' % time.time()

        if os.path.exists(directory) is False:
            os.mkdir(directory)

        self.directory = os.path.join(directory)

        basedir = os.path.abspath(os.path.dirname(__file__))
        os.system('cp -f ' + basedir + "/../../../fixture/build-composer-cc2632fae2cab2f73ce6e6607d9b0befec0b82a1.tar.gz" +
                  " " +
                  self.directory)

        return self.directory

    def remove_fixture(self):
        if os.path.exists(self.directory) is True:
            os.system('rm -rf ' + self.directory)
