import httpretty
import pytest
from middleware.gitlab.download import Download


class TestDownload(object):
    def test_get_latest_version_not_found(self):
        httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
        httpretty.register_uri(httpretty.GET,
                               "https://localhost/api/v3/projects/web-jenkins-jobs%2Funit-tests-codeception/repository/tags?private_token=123456",
                               status=404)

        gitlab = Download(self.get_data())

        with pytest.raises(Exception) as inst:
            gitlab.get_latest_version("unit-tests-codeception")
        assert str(
            inst.value) == "It was not possible to get the tags for abstract job unit-tests-codeception in gitlab."

    def test_get_latest_version(self):
        httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
        httpretty.register_uri(httpretty.GET,
                               "https://localhost/api/v3/projects/web-jenkins-jobs%2Funit-tests-codeception/repository/tags?private_token=123456",
                               body=self.get_gitlab_responnse(),
                               status=200)

        gitlab = Download(self.get_data())
        gitlab.get_latest_version("unit-tests-codeception") is "v1.1.1"

    def test_get_latest_version_return_none(self):
        httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
        httpretty.register_uri(httpretty.GET,
                               "https://localhost/api/v3/projects/web-jenkins-jobs%2Funit-tests-codeception/repository/tags?private_token=123456",
                               body="{}",
                               status=200)

        gitlab = Download(self.get_data())
        gitlab.get_latest_version("unit-tests-codeception") is None

    @classmethod
    def get_data(cls):
        return {
            "host": "https://localhost",
            "tag_path": "api/v3/projects/web-jenkins-jobs%2F{}/repository/tags?private_token={}",
            "private_token": "123456"
        }

    @classmethod
    def get_gitlab_responnse(cls):
        return """
[
    {
        "name": "v1.1.1",
        "message": null,
        "commit": {
            "id": "39458e73731ab1fd967ae7b2fa77961ae00a2ed1",
            "message": "Merge branch 'develop' into 'master'Fixed not deployed issue.See merge request !26",
            "parent_ids": ["167ae1a999a7b425dd4cc38478272aa994253611", "e79fb58f596e19f81906a733cd37692a4a365da7"],
            "authored_date": "2015-06-18T11:24:16.000+02:00",
            "author_name": "Tobias Wiesenthal",
            "author_email": "twiesenthal@goodgamestudios.com",
            "committed_date": "2015-06-18T11:24:16.000+02:00",
            "committer_name": "Tobias Wiesenthal",
            "committer_email": "twiesenthal@goodgamestudios.com"
        }
    },
    {
        "name": "v1.1.0",
        "message": null,
        "commit": {
            "id": "32df1bed88994242ec1a51585f12cf65990f0432",
            "message": "Merge branch 'develop' into 'master'Showing last successful deployed packageSee merge request !22",
            "parent_ids": ["d0bda709a892b64d7535add47c9b843c8d8f0bc0", "32b1acb8509969cb05e467907611acba286a0482"],
            "authored_date": "2015-06-17T11:31:08.000+02:00",
            "author_name": "Tobias Wiesenthal",
            "author_email": "twiesenthal@goodgamestudios.com",
            "committed_date": "2015-06-17T11:31:08.000+02:00",
            "committer_name": "Tobias Wiesenthal",
            "committer_email": "twiesenthal@goodgamestudios.com"
        }
    },
    {
        "name": "v1.0.2",
        "message": null,
        "commit": {
            "id": "c0e1ba7d5bf91519ee1bed8190fdc7050d02dc3b",
            "message": "updated CHANGELOG.md",
            "parent_ids": ["0b1241d01a7e227fbe5763a8ea9f6a82030f15a5"],
            "authored_date": "2015-06-16T11:16:31.000+02:00",
            "author_name": "Tobias Wiesenthal",
            "author_email": "twiesenthal@goodgamestudios.com",
            "committed_date": "2015-06-16T11:16:31.000+02:00",
            "committer_name": "Tobias Wiesenthal",
            "committer_email": "twiesenthal@goodgamestudios.com"
        }
    },
    {
        "name": "v1.0.1",
        "message": null,
        "commit": {
            "id": "fd555d4b2d036e8d5fe712a912c924fddc4e2ec5",
            "message": "Merge branch 'develop' into 'master'Getting the urls dynamicallySee merge request !16",
            "parent_ids": ["6b8a70a1719f6ca44229cc80c26aeb6bfdf00109", "a7664a55ba8ab15664176d4debda7778f6fe119f"],
            "authored_date": "2015-06-12T08:44:58.000+02:00",
            "author_name": "Tobias Wiesenthal",
            "author_email": "twiesenthal@goodgamestudios.com",
            "committed_date": "2015-06-12T08:44:58.000+02:00",
            "committer_name": "Tobias Wiesenthal",
            "committer_email": "twiesenthal@goodgamestudios.com"
        }
    },
    {
        "name": "v1.0.0",
        "message": null,
        "commit": {
            "id": "6b8a70a1719f6ca44229cc80c26aeb6bfdf00109",
            "message": "Merge branch 'develop' into 'master'DevelopSee merge request !15",
            "parent_ids": ["288972ff0b9f74a7d0f236c90b1974925cb72bb1", "6494eb41723481dc6a8194791666a0fc2389d8b5"],
            "authored_date": "2015-05-28T11:55:44.000+02:00",
            "author_name": "Alberto GuimarÃ£es Viana",
            "author_email": "aguimaraesviana@goodgamestudios.com",
            "committed_date": "2015-05-28T11:55:44.000+02:00",
            "committer_name": "Alberto GuimarÃ£es Viana",
            "committer_email": "aguimaraesviana@goodgamestudios.com"
        }
    }]
"""
