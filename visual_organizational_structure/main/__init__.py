from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='templates')

from visual_organizational_structure.main import routes