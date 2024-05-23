from flask import Blueprint

bp = Blueprint('settings', __name__, template_folder='templates')

from visual_organizational_structure.settings import routes