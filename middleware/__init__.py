from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    app.config.from_object('config')

    # initialize database
    db.init_app(app)

    # register blueprints
    from .jenkins import api_jenkins as api_jenkins_blueprint
    app.register_blueprint(api_jenkins_blueprint, url_prefix='/api/jenkins')

    return app
