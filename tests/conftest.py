from unittest.mock import MagicMock
import pytest
from app import app
from dao.director import DirectorDAO
from dao.genre import GenreDAO
from dao.models import User
from dao.user import UserDAO
from db_utils.setup_db import db as database
from service.auth import AuthService
from service.user import UserService


@pytest.fixture()
def flask_app():
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        DEBUG=False
    )
    with app.app_context():
        yield app


@pytest.fixture()
def db(flask_app):
    database.init_app(flask_app)
    database.create_all()

    yield database

    database.session.close()


@pytest.fixture
def client(flask_app, db):
    with app.test_client() as client:
        yield client


@pytest.fixture
def director_dao(db):
    return DirectorDAO(db.session)


@pytest.fixture
def genre_dao(db):
    return GenreDAO(db.session)


@pytest.fixture
def user_dao(db):
    return UserDAO(db.session)


@pytest.fixture
def get_user_token(user_dao):
    test_user = User(id=1, email='test@mail.ru', password=UserService(user_dao).get_hash("qwert_@Y"))
    UserService.get_by_email = MagicMock(return_value=test_user)
    AuthService.get_user_by_token = MagicMock(return_value=test_user)
    token = AuthService(UserService(user_dao)).generate_tokens(
        email=test_user.email,
        password="qwert_@Y"
    )["access_token"]
    return token
