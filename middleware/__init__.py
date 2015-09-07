from configparser import ConfigParser

from flask import Flask, make_response
from flask_restful import Api
from flask.json import jsonify
from os import path

app = Flask(__name__)
api = Api(app)

"""
Loading configuration
"""
configuration = ConfigParser()
configuration.read(path.abspath(path.dirname(__file__)) + '/../config.ini')


@app.errorhandler(404)
def not_found(error):
    """
    Error 404 is returning a json
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


from middleware.jenkins.controllers import Controllers as JenkinsController

api.add_resource(JenkinsController, '/api/jenkins/pipeline')
