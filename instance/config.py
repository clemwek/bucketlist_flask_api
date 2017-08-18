import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    PORT = 5000
    SECRET_KEY = os.getenv('SECRET', 'my_precious')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:newpassword@localhost/test_flask_api'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
