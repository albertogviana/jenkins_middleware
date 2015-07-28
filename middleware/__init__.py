from flask import Flask
from flask_restful import Resource, Api
from middleware.jenkins.controllers import Controllers


app = Flask(__name__)
api = Api(app)

api.add_resource(Controllers, '/pipeline')
