from decouple import *
from flask import Flask# TO DO: fix the import

from flask_migrate import Migrate
from flask_restful import Api

from backend.resources.routes import routes
from db import db


try:
    env_config = Config(RepositoryEnv('.env'))
except FileNotFoundError:
    from decouple import config as env_config



class DevelopmentConfig:
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{env_config('DB_USER')}:{env_config('DB_PASSWORD')}"
        f"@{env_config('DB_HOST')}:{env_config('DB_PORT')}/{env_config('DB_NAME')}"
    )

class TestingConfig:
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # in-memory DB



def create_app(config = 'config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)

    api = Api(app)
    migrate = Migrate(app, db)


    [api.add_resource(*route) for route in routes]
    return app
