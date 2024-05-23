from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates')

from visual_organizational_structure.auth import routes