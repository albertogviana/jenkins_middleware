from flask import Blueprint

api_jenkins = Blueprint('api_jenkins', __name__)

from . import controllers, errors, models
