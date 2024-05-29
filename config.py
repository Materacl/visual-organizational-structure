from os import environ, path

BASE_DIR = path.abspath(path.dirname(__file__))


class Config:
    """Flask configuration variables."""
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = environ.get('SECRET_KEY')
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = environ.get('REDIS_URL')


class TestConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CACHE_TYPE = 'SimpleCache'
