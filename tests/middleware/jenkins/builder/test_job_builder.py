from unittest.mock import Mock
from middleware.gitlab.download import Download


class TestJobBuilder(object):
    def test_get_archieve(self):
        download = Download(self.get_data())
        download.get_archieve = Mock(return_value="/Users/alberto/Documents/Projects/docker/jenkins_middleware/tests/fixture/start-cbab6de129fdece998a7aa1c4f6e8be34d2170be.tar.gz")
        assert download.get_archieve("python-test", "unit-tests-codeception", "v*") is "/Users/alberto/Documents/Projects/docker/jenkins_middleware/tests/fixture/start-cbab6de129fdece998a7aa1c4f6e8be34d2170be.tar.gz"

    @classmethod
    def get_data(cls):
        return {
            "host": "https://localhost",
            "tag_path": "api/v3/projects/web-jenkins-jobs%2F{}/repository/tags?private_token={}",
            "private_token": "123456",
            "download_path": "web-jenkins-jobs/{}/repository/archive.tar.gz?ref={}"
        }