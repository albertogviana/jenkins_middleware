from middleware.jenkins.parser.parser import Parser
import pytest


class TestParser(object):
    def test_get_json_data(self):
        json = self._get_data()
        parser = Parser(json)
        assert parser.get_json_data() is json

    def test_get_name(self):
        parser = Parser(self._get_data())
        assert parser.get_name() == "python-test"

    def test_get_abstract_name(self):
        parser = Parser(self._get_data())
        assert parser.get_abstract_name() == "unit-tests-codeception"

    def test_get_abstract_version(self):
        parser = Parser(self._get_data())
        assert parser.get_abstract_version() == "v*"

    def test_get_job_parameter_job_not_found(self):
        parser = Parser({})
        with pytest.raises(Exception) as inst:
            parser.get_job_parameter('version')
        assert str(inst.value) == "Job field was not found."

    def test_get_job_parameter_field_not_found(self):
        parser = Parser(self._get_data())
        with pytest.raises(Exception) as inst:
            parser.get_job_parameter('my-field')
        assert str(inst.value) == "my-field field was not found."

    def test_get_placeholders(self):
        parser = Parser(self._get_data())
        placeholders = {
            "PATH_OF_CODECEPTIONS_YML": "codeception.yml",
            "UPSTREAM_PROJECT": "my-upstream-project",
            "DOWNSTREAM_PROJECT": "my-downstream-project",
            "CODECEPTION_ENVIRONMENT": "test"
        }
        assert parser.get_placeholders() == placeholders

    def test_get_placeholders_placeholder_not_found(self):
        parser = Parser({})
        with pytest.raises(Exception) as inst:
            parser.get_placeholders()
        assert str(inst.value) == "Placeholder field was not found."

    def test_get_placeholder(self):
        parser = Parser(self._get_data())
        assert parser.get_placeholder("UPSTREAM_PROJECT") == "my-upstream-project"

    def test_get_placeholder_placeholder_not_found(self):
        parser = Parser(self._get_data())
        with pytest.raises(Exception) as inst:
            parser.get_placeholder('test')
        assert str(inst.value) == "test field was not found."

    @classmethod
    def _get_data(cls):
        return {
            "format_version": "1.0",
            "job": {
                "name": "python-test",
                "abstract_name": "unit-tests-codeception",
                "version": "v*"
            },
            "placeholder": {
                "PATH_OF_CODECEPTIONS_YML": "codeception.yml",
                "UPSTREAM_PROJECT": "my-upstream-project",
                "DOWNSTREAM_PROJECT": "my-downstream-project",
                "CODECEPTION_ENVIRONMENT": "test"
            }
        }
