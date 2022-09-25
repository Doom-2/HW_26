import json
import os
from unittest.mock import MagicMock
import pytest
from dao.models import User, Genre
from dao.user import UserDAO
from service.auth import AuthService
from service.user import UserService


class TestRoutes:

    @pytest.fixture
    def genre(self, db):
        obj = Genre(name="genre")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_user_page_not_logged_in(self, client, user_dao):
        res = client.get('/user')
        assert res.status_code == 401

    def test_root_status(self, client) -> None:
        """ Checking whether the desired status code is obtained """
        response = client.get('/', follow_redirects=True)
        assert response.status_code == 200, "Status code is wrong"

    def test_get_single_genre(self, client, genre, get_user_token):
        response = client.get(
            "/genres/1/",
            headers={'Authorization': f'Bearer {get_user_token}'},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert response.json == {"id": genre.id, "name": genre.name}

    def test_get_user_favorite_movies(self, client, get_user_token) -> None:
        """ Checking whether the desired status code is obtained """
        response = client.get(
            '/favorites/movies',
            headers={'Authorization': f'Bearer {get_user_token}'},
            follow_redirects=True
        )
        assert response.status_code == 200, "Status code is wrong"

    def test_post(self, client):
        headers = {'Content-Type': 'application/json'}
        data = {"name": "yet non-existent director\'s name"}
        response = client.post("/directors/", data=json.dumps(data), headers=headers)
        assert response.status_code == 201, "Status code is wrong"


if __name__ == "__main__":
    os.system("pytest")
