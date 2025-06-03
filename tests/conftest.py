import pytest
from config import TestingConfig, create_app
from db import db

@pytest.fixture(scope='session')
def app():
    app = create_app(config=TestingConfig)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def session(app):
    connection = db.engine.connect()
    transaction = connection.begin()

    db.session.bind = connection

    yield db.session

    db.session.remove()
    transaction.rollback()
    connection.close()
