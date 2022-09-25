import os
import pytest
from dao.models import Genre


class TestGenresDAO:
    @pytest.fixture
    def genre_1(self, db):
        genre_1 = Genre(name="Боевик")
        db.session.add(genre_1)
        db.session.commit()
        return genre_1

    @pytest.fixture
    def genre_2(self, db):
        genre_2 = Genre(name="Комедия")
        db.session.add(genre_2)
        db.session.commit()
        return genre_2

    def test_get_one_genre(self, genre_1, genre_dao):
        assert genre_dao.get_one(genre_1.id) == genre_1

    def test_get_one_genre_not_found(self, genre_dao):
        assert not genre_dao.get_one(1)

    def test_get_all_genres(self, genre_dao, genre_1, genre_2):
        assert genre_dao.get_all() == [genre_1, genre_2]

    def test_get_genres_by_page(self, flask_app, genre_dao, genre_1, genre_2):
        flask_app.config['ITEMS_PER_PAGE'] = 1
        assert genre_dao.get_all(page=1) == [genre_1]
        assert genre_dao.get_all(page=2) == [genre_2]
        assert genre_dao.get_all(page=3) == []

    def test_create_a_genre(self, db, genre_dao):
        genre_data = {
            "name": "Комедия"
        }
        new_genre = Genre(**genre_data)
        db.session.add(new_genre)
        db.session.commit()
        assert new_genre.name == genre_data["name"]
        assert new_genre.id == 1


if __name__ == "__main__":
    os.system("pytest")
