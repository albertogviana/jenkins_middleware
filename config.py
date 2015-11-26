import os

basedir = os.path.abspath(os.path.dirname(__file__))

"""
Loading configuration
"""

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'cimiddleware.db')

GITLAB_CONFIGURATION = {
    "host": "",
    "tag_path": "api/v3/projects/%2F{}/repository/tags?private_token={}",
    "download_path": "/{}/repository/archive.tar.gz?ref={}",
    "private_token": ""
}

JENKINS_USER = "jenkins"
JENKINS_KEY_FILE = ""

OPENSSH_CONFIGURATION = {
    "user": JENKINS_USER,
    "key_file": JENKINS_KEY_FILE
}

# SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True to suppress this warning.
SQLALCHEMY_TRACK_MODIFICATIONS = True

LOG_FOLDER = os.path.join(basedir, 'log')
LOG_FILENAME = os.path.join(LOG_FOLDER, 'octopus.log')
