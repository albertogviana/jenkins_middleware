from flask import request, current_app
from flask.json import jsonify
from . import api_jenkins
from .facade import Facade
from ..exceptions import ValidationError
from werkzeug.exceptions import HTTPException, NotFound


@api_jenkins.route('/pipeline', methods=['POST'])
def handle_pipeline():
    try:
        data = request.json
# response = Facade(current_app.config).process(data)
        response = Facade(current_app.config).process(data)
        # print(response)
    # except ValueError as inst:
    #     print("here")
    #     return inst
    # except ValueError as inst:
    #     print('ValueError')
    #     print(inst)
    #     return inst
    except HTTPException as e:
        print('http')
        print(e.name)
        # reponse = jsonify({'status': e.code, 'error': e.name, 'message': e.description})
        # response.status = e.code
        return {'message': e.description}, e.code
        # return response
    except Exception as e:
        print(str(e))
        return jsonify(e)
    return response
