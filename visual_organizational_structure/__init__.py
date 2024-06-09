"""Initialize Flask app."""
from config import Config

from flask import Flask

from visual_organizational_structure.database import db, migrate
from visual_organizational_structure.utils import manager, mail, cache


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    manager.init_app(app)
    mail.init_app(app)
    cache.init_app(app, config={
        'CACHE_TYPE': Config.CACHE_TYPE,
        'CACHE_REDIS_URL': Config.CACHE_REDIS_URL
    })
    
    from visual_organizational_structure.main import bp as main_bp
    app.register_blueprint(main_bp)

    from visual_organizational_structure.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from visual_organizational_structure.dashboards import bp as dashboards_bp
    app.register_blueprint(dashboards_bp)

    from visual_organizational_structure.settings import bp as settings_bp
    app.register_blueprint(settings_bp)

    from visual_organizational_structure.dash_apps.organization_graph import init_dashboard
    init_dashboard(app)

    with app.app_context():
        db.create_all()

    return app