from middleware.openssh.ssh import Ssh
import pytest


class TestSsh(object):
    def test_ssh_exception_user(self):
        with pytest.raises(Exception) as inst:
            Ssh({"OPENSSH_CONFIGURATION":{}})
        assert str(inst.value) == "User parameter is required for ssh."

    def test_ssh_exception_key_file(self):
        with pytest.raises(Exception) as inst:
            Ssh({"OPENSSH_CONFIGURATION": {"user": "user"}})
        assert str(inst.value) == "Key file is required for ssh."

    def test_get_host_exception(self):
        ssh = Ssh(self.get_data())
        with pytest.raises(Exception) as inst:
            ssh._get_host("abcde123445")
        assert str(inst.value) == "The host abcde123445 informed is not valid for ssh."

    def test_get_host(self):
        ssh = Ssh(self.get_data())
        assert ssh._get_host("http://localhost/index") == "localhost"
        assert ssh._get_host("https://localhost/index") == "localhost"

    def test_parse(self):
        result = r'/usr/bin/ssh -i test_file -o StrictHostKeyChecking=no user@jenkins.backend.com "bash -c \"if [ ! -d {jenkins}/{folder} ]; then  mkdir -p {jenkins}/{folder}; fi\""'
        ssh = Ssh(self.get_data())
        execute_command = r'"bash -c \"if [ ! -d {jenkins}/{folder} ]; then  mkdir -p {jenkins}/{folder}; fi\""'
        command = ssh._parse('http://jenkins.backend.com/', execute_command)
        assert result == command

    #
    def test_execute_host_exception(self):
        ssh = Ssh(self.get_data())
        with pytest.raises(Exception) as inst:
            ssh.execute('', '')
        assert str(inst.value) == "The host parameter could not be empty on ssh."

    def test_execute_shell_script_exception(self):
        ssh = Ssh(self.get_data())

        with pytest.raises(Exception) as inst:
            ssh.execute('http://localhost', '')
        assert str(inst.value) == "The shell script parameter could not be empty on ssh."

    @classmethod
    def get_data(cls):
        return {
            "OPENSSH_CONFIGURATION": {
                "user": "user",
                "key_file": "test_file"
            }
        }
