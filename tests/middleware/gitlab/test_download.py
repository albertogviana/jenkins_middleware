import httpretty
import pytest
from middleware.gitlab.download import Download


class TestDownload(object):
    def test_get_latest_version_not_found(self):
        httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
        httpretty.register_uri(httpretty.GET,
                               "https://localhost/api/v3/projects/web-jenkins-jobs%2Funit-tests-codeception/repository/tags?private_token=123456",
                               status=404)

        configuration = {
            "host": "https://localhost",
            "tag_path": "api/v3/projects/web-jenkins-jobs%2F{}/repository/tags?private_token={}",
            "private_token": "123456"
        }

        gitlab = Download(configuration)

        with pytest.raises(Exception) as inst:
            gitlab.get_latest_version("unit-tests-codeception")
        assert str(
            inst.value) == "It was not possible to get the tags for abstract job unit-tests-codeception in gitlab."
