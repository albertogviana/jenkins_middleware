from flask import Blueprint

api_gitlab = Blueprint('api_gitlab', __name__)

from . import controllers, web_hook
