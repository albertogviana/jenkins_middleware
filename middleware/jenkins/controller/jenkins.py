from flask_restful import Resource
from flask import request
from flask.json import jsonify
from middleware.jenkins.services.jenkins_facade import JenkinsFacade
from middleware import app

class Jenkins(Resource):
    """
    Jenkins Controller
    """

    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            return jsonify(JenkinsFacade(app.config).process(data))
        except Exception as inst:
            return jsonify({'message': inst.args})
