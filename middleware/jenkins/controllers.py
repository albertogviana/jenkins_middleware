from flask import request, current_app
from flask.json import jsonify
from . import api_jenkins
from .facade import Facade


@api_jenkins.route('/pipeline', methods=['POST'])
def handle_pipeline():
    print(request.json)
    response = Facade(current_app.config).process(request.json)
    return jsonify(response)
