import os
from unittest.mock import MagicMock
import pytest
from dao.models import Genre
from dao.genre import GenreDAO
from service.genre import GenreService


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)

    test_genre_1 = Genre(id=1, name='Драма')
    test_genre_2 = Genre(id=2, name='Фантастика')
    test_genre_3 = Genre(id=3, name='Триллер')

    genre_dao.get_all = MagicMock(return_value=[test_genre_1, test_genre_2, test_genre_3])
    genre_dao.get_one = MagicMock(return_value=test_genre_1)
    genre_dao.create = MagicMock(return_value=Genre(id=2))
    genre_dao.update = MagicMock()
    genre_dao.delete = MagicMock()
    return genre_dao


class TestGenreService:

    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_all(self):
        all_genres = self.genre_service.get_all()

        assert len(all_genres) > 0

    def test_get_one(self):
        single_genre = self.genre_service.get_one(2)

        assert single_genre is not None
        assert single_genre.id is not None

    def test_create(self):
        genre_data = {
            "name": "Ужасы"
        }

        new_genre = self.genre_service.create(genre_data)

        assert new_genre.id is not None

    def test_update(self):
        genre_data = {
            "name": "Комедия"
        }

        new_genre = self.genre_service.create(genre_data)

        assert new_genre.id is not None

    def test_delete(self):
        assert self.genre_service.delete(2) is None


if __name__ == "__main__":
    os.system("pytest")
