"""Initialize Flask app."""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
manager = LoginManager()
migrate = Migrate()
mail = Mail()

def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345678@localhost:5432/test db'
        #'sqlite:///../instance/my_database.db'
    app.config['SECRET_KEY'] = 'test_key'
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'dzozefkramber@gmail.com'
    app.config['MAIL_DEFAULT_SENDER'] = 'dzozefkramber@gmail.com'
    app.config['MAIL_PASSWORD'] = 'mqheegfsfbcbnltw'
    mail = Mail(app)
    db.init_app(app)
    migrate.init_app(app, db)
    manager.init_app(app)

    with app.app_context():
        db.create_all()  # Create database tables

        # Import parts of our core Flask app
        from . import routes

        # Import Dash application
        from .dash_apps.organization_graph.dashboard import init_dashboard
        app = init_dashboard(app)

        return app
