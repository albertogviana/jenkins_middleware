from flask import Flask, make_response
from flask_restful import Api
from flask.json import jsonify
from middleware.jenkins.controllers import Controllers


app = Flask(__name__)
api = Api(app)

api.add_resource(Controllers, '/pipeline')

"""
Error 404 is returning a json
"""
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)