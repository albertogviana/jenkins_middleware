from flask import request, current_app
from flask.json import jsonify
from .web_hook import WebHook
from . import api_gitlab


@api_gitlab.route('/pushes', methods=['POST'])
def push():
    response = WebHook(app=current_app.config, logger=current_app.logger).push(request.json)
    return jsonify(response), 200