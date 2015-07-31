from flask_restful import Resource
from flask import request
from flask.json import jsonify
from middleware.jenkins.jenkins_facade import JenkinsFacade


class Controllers(Resource):
    def post(self):
        try:
            data = request.get_json()
            return jsonify(JenkinsFacade().create(data))
        except Exception as inst:
            return jsonify({'message': inst.args})
