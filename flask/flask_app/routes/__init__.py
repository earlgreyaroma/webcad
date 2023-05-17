from flask import Blueprint

user_bp = Blueprint('user_bp', __name__)
admin_bp = Blueprint('admin_bp', __name__)
error_bp = Blueprint('error_bp', __name__)

from .admin_routes import *
from .user_routes import *
from .error_routes import *