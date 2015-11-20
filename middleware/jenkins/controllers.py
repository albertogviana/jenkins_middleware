from flask import request, current_app
from flask.json import jsonify
from . import api_jenkins
from middleware.jenkins.facade import Facade


@api_jenkins.route('/create-pipeline', methods=['POST'])
def handle_pipeline():
    response = Facade(app=current_app.config, logger=current_app.logger).process(request.json)
    return jsonify(response), 201
