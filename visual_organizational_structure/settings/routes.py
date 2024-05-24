from flask import render_template
from visual_organizational_structure.settings import bp


@bp.route("/settings")
def settings():
    return render_template("settings.jinja2")
