from flask_restful import Resource
from flask.json import jsonify


class Controllers(Resource):
    def post(self):
        return jsonify(name="Mozão love <3 Mozinho!")
