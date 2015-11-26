import logging
from unittest.mock import Mock

import pytest
from middleware.gitlab.web_hook import WebHook


class TestWebHook(object):
    def test_get_pipeline_type(self):
        logger_mock = logging
        logger_mock.info = Mock(True)
        webhook = WebHook({}, logger_mock)
        assert webhook.get_pipeline_type("master") == "master"
        assert webhook.get_pipeline_type("develop") == "develop"
        assert webhook.get_pipeline_type("release-test") == "release"
        assert webhook.get_pipeline_type("release-test.1.1.2") == "release"
        assert webhook.get_pipeline_type("release/test") == "release"
        assert webhook.get_pipeline_type("release/test.1.1.2") == "release"
        assert webhook.get_pipeline_type("hotfix-test") == "release"
        assert webhook.get_pipeline_type("hotfix-test1.1.3") == "release"
        assert webhook.get_pipeline_type("hotfix/test") == "release"
        assert webhook.get_pipeline_type("hotfix/test1.1.3") == "release"
        assert webhook.get_pipeline_type("feature-test") == "feature"
        assert webhook.get_pipeline_type("feature-test1.2.4") == "feature"
        assert webhook.get_pipeline_type("feature/test") == "feature"
        assert webhook.get_pipeline_type("feature/test.1.2.4") == "feature"

    def test_get_pipeline_type_exception(self):
        logger_mock = logging
        logger_mock.error = Mock(True)
        webhook = WebHook({}, logger_mock)

        with pytest.raises(Exception) as inst:
            webhook.get_pipeline_type("exception-test")
        assert str(inst.value) == "The branch exception-test is not follow the name convention."
