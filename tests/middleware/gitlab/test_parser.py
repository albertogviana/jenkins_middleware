from middleware.gitlab.parser import Parser


class TestParser(object):
    def test_get_repository_namespace(self):
        parser = Parser(self._get_data())
        assert parser.get_repository_namespace() == "web-conversion"

        parser2 = Parser({})
        assert parser2.get_repository_namespace() == ""

    def test_get_repository_url(self):
        parser = Parser(self._get_data())
        assert parser.get_repository_url() == "git@source.services.ggs-net.com:web-conversion/lp-toolbox.git"

        parser2 = Parser({})
        assert parser2.get_repository_url() == ""

    def test_get_branch_name(self):
        parser = Parser(self._get_data())
        assert parser.get_branch_name() == "master"

        parser2 = Parser({"ref": "refs/heads/feature-test"})
        assert parser2.get_branch_name() == "feature-test"

    def test_get_project_name(self):
        parser = Parser(self._get_data())
        assert parser.get_project_name() == "lp-toolbox"

        parser2 = Parser({})
        assert parser2.get_branch_name() == ""

    @classmethod
    def _get_data(cls):
        return {
            "before": "95790bf891e76fee5e1747ab589903a6a1f80f22",
            "after": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
            "ref": "refs/heads/master",
            "user_id": 4,
            "user_name": "John Smith",
            "project_id": 15,
            "repository": {
                "name": "lp-toolbox",
                "url": "git@source.services.ggs-net.com:web-conversion/lp-toolbox.git",
                "description": "",
                "homepage": "http://example.com/web-conversion"
            },
            "commits": [
                {
                    "id": "b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
                    "message": "Update Catalan translation to e38cb41.",
                    "timestamp": "2011-12-12T14:27:31+02:00",
                    "url": "http://example.com/team42/commits/b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
                    "author": {
                        "name": "Jordi Mallach",
                        "email": "jordi@softcatala.org"
                    }
                },
                {
                    "id": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
                    "message": "fixed readme",
                    "timestamp": "2012-01-03T23:36:29+02:00",
                    "url": "http://example.com/team42/commits/da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
                    "author": {
                        "name": "GitLab dev user",
                        "email": "gitlabdev@dv6700.(none)"
                    }
                }
            ],
            "total_commits_count": 4
        }
