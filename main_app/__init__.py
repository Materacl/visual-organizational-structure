"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
manager = LoginManager()


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SECRET_KEY'] = 'test_key'
    db.init_app(app)
    manager.init_app(app)

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        # Import Dash application
        from .dash_apps.organization_graph.dashboard import init_dashboard
        app = init_dashboard(app)

        return app
