
class BaseConfig(object):
    port = 5000
    SECRET_KEY = '1233211234567'

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG = True

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///GRSystemData.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///GRSystemData.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}