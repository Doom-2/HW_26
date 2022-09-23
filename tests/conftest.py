import pytest
from flask.testing import FlaskClient
from app import app


@pytest.fixture(scope='module')
def flask_app():
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def client(flask_app):
    app = flask_app
    ctx = flask_app.test_request_context()
    ctx.push()
    app.test_client_class = FlaskClient
    return app.test_client()
