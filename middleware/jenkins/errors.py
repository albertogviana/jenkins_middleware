from flask import jsonify
from . import api_jenkins


@api_jenkins.app_errorhandler(400)
def bad_request(exception):
    """
    Bad Request json response
    """
    response = jsonify({'status': 400, 'error': 'bad request', 'message': exception.description})
    response.status_code = 400
    return response

@api_jenkins.app_errorhandler(403)
def forbidden(exception):
    """
    Internal Server Error json response
    """
    response = jsonify({'status': 403, 'error': 'forbidden',
                        'message': exception.description})
    response.status_code = 403
    return response

@api_jenkins.app_errorhandler(404)  # this has to be an app-wide handler
def not_found(exception):
    """
    Not Found json response
    """
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': 'invalid resource URI'})
    response.status_code = 404
    return response


@api_jenkins.app_errorhandler(405)
def method_not_supported(exception):
    """
    Methond Not Supported json response
    """
    response = jsonify({'status': 405, 'error': 'method not supported',
                        'message': 'the method is not supported'})
    response.status_code = 405
    return response


@api_jenkins.app_errorhandler(422)
def unprocessable_entity(exception):
    """
    Internal Server Error json response
    """
    response = jsonify({'status': 422, 'error': 'unprocessable entity',
                        'message': exception.description})
    response.status_code = 422
    return response


@api_jenkins.app_errorhandler(500)  # this has to be an app-wide handler
def internal_server_error(exception):
    """
    Internal Server Error json response
    """
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': exception.args[0]})
    response.status_code = 500
    return response
