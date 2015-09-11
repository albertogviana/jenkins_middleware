from configparser import ConfigParser

import os

basedir = os.path.abspath(os.path.dirname(__file__))

CONFIGURATION_FILE = 'config.ini'

if not os.path.isfile(os.path.join(basedir, CONFIGURATION_FILE)):
    raise Exception('Configuration file was not found.')

"""
Loading configuration
"""
configuration = ConfigParser()
configuration.read(os.path.join(basedir, CONFIGURATION_FILE))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'cimiddleware.db')