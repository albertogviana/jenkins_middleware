from flask import Flask, make_response
from flask_restful import Api
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from config import configuration


app = Flask(__name__)
app.config.from_object(configuration)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

from middleware.jenkins.controller.jenkins import Jenkins as JenkinsController
from middleware.jenkins.model.configuration import Configuration as ConfigurationEntity


@app.errorhandler(404)
def not_found():
    """
    Error 404 is returning a json
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


api.add_resource(JenkinsController, '/api/jenkins/pipeline')
