from flask import render_template, request
from visual_organizational_structure.main import bp


@bp.route("/")
def home():
    """Home page of Flask Application."""
    return render_template(
        "index.jinja2",
        title="Home page",
        description="Home page.",
        template="home-template",
        body="This is a homepage served with Flask.",
        base_url=request.base_url,
    )
