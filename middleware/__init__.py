from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import configuration

db = SQLAlchemy()


# app.config.from_object('config')

# api = Api(app)

# from middleware.jenkins.controller import Jenkins as JenkinsController
# from middleware.jenkins.models import Configuration as ConfigurationEntity


# @app.errorhandler(404)
# def not_found():
#     """
#     Error 404 is returning a json
#     """
#     return make_response(jsonify({'error': 'Not found'}), 404)
# api.add_resource(JenkinsController, '/api/jenkins/pipeline')

def create_app():
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    app.config.from_object(configuration)
    app.config.from_object('config')

    # initialize database
    db.init_app(app)

    # register blueprints
    from .jenkins import api_jenkins as api_jenkins_blueprint
    app.register_blueprint(api_jenkins_blueprint, url_prefix='/api/jenkins')

    return app
