from flask import Blueprint

manage = Blueprint('manage', __name__)

from . import views