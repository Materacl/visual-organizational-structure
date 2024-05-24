from flask_login import LoginManager
from flask_mail import Mail
from flask_caching import Cache

manager = LoginManager()
mail = Mail()
cache = Cache()
