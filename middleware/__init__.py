from logging import getLogger, Formatter, INFO
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Create an application instance."""
    app = Flask(__name__)
    app.config.from_object('config')

    formatter = Formatter("[%(asctime)s] %(pathname)s:%(lineno)d %(levelname)s - %(message)s")
    file_handler = RotatingFileHandler(app.config["LOG_FILENAME"], maxBytes=10000000, backupCount=5)
    app.logger.setLevel(INFO)
    file_handler.setLevel(INFO)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    app.logger.info('octopus startup')

    # initialize database
    db.init_app(app)

    # register blueprints
    from .jenkins import api_jenkins as api_jenkins_blueprint
    app.register_blueprint(api_jenkins_blueprint, url_prefix='/api/jenkins')

    from .gitlab import api_gitlab as api_gitlab_blueprint
    app.register_blueprint(api_gitlab_blueprint, url_prefix='/api')

    return app
