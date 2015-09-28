from middleware.openssh.scp import Scp
import pytest


class TestScp(object):
    def test_scp_exception_user(self):
        with pytest.raises(Exception) as inst:
            Scp({})
        assert str(inst.value) == "User parameter is required for scp."

    def test_scp_exception_key_file(self):
        with pytest.raises(Exception) as inst:
            Scp({"user": "user"})
        assert str(inst.value) == "Key file is required for scp."

    def test_get_host_exception(self):
        scp = Scp(self.get_data())
        with pytest.raises(Exception) as inst:
            scp._get_host("abcde123445")
        assert str(inst.value) == "The host abcde123445 informed is not valid for scp."

    def test_get_host(self):
        scp = Scp(self.get_data())
        assert scp._get_host("http://localhost/index") == "localhost"
        assert scp._get_host("https://localhost/index") == "localhost"

    def test_parse(self):
        result = '/usr/bin/scp -o StrictHostKeyChecking=no -o ConnectTimeout=10 -i test_file -r /var/www user@jenkins.backend.com:/var/www/my-project 2>&1'
        scp = Scp(self.get_data())
        command = scp._parse('/var/www', '/var/www/my-project', 'http://jenkins.backend.com/')
        assert result == command

    def test_execute_source_exception(self):
        scp = Scp(self.get_data())
        with pytest.raises(Exception) as inst:
            scp.execute('', '', '')
        assert str(inst.value) == "The source parameter could not be empty on scp."

    def test_execute_destination_exception(self):
        scp = Scp(self.get_data())

        with pytest.raises(Exception) as inst:
            scp.execute('/var/www', '', '')
        assert str(inst.value) == "The destination parameter could not be empty on scp."

    def test_execute_host_exception(self):
        scp = Scp(self.get_data())

        with pytest.raises(Exception) as inst:
            scp.execute('/var/www', '/var/www/my-project', '')
        assert str(inst.value) == "The host parameter could not be empty on scp."

    @classmethod
    def get_data(cls):
        return {
            "user": "user",
            "key_file": "test_file"
        }
