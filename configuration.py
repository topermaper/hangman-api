import os
import datetime

class BaseConfig(object):
    #Flask Configuration
    # SECRET KEY to be set as environment variable in production
    SECRET_KEY = 'SECRET_KEY'
    JWT_SECRET_KEY = 'JWT_SECRET_KEY'
    CSRF_SECRET_KEY = 'CSRF_SECRET_KEY'

    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI='sqlite:///database.db'

    # Game configuration
    WORD_LIST = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
    ALLOWED_MISSES = 4

    # API configuration
    BASE_API_URL     = '/api/v1'

    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=600)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=3600)

class ProductionConfig(BaseConfig):
    DEBUG = False
    
    JWT_COOKIE_CSRF_PROTECT = True
    # SECRET KEY to be set as environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SERVER_NAME="productionhost.changeme:50011"

class DevelopmentConfig(BaseConfig):
    ENV= 'development'
    DEBUG = True
    TESTING = True
    SERVER_NAME="localhost.localdomain:50011"
