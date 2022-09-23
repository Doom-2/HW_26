import os
from unittest.mock import MagicMock
import pytest
from dao.models import Movie
from dao.movie import MovieDAO
from service.movie import MovieService

# This classes are imported to prevent error related to linked 'director' and 'genre' tables while testing
from dao.models import Director
from dao.models import Genre


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    test_movie_1 = Movie(id=1,
                         title='Сталкер',
                         description='Глубоко философская картина А.Тарковского про'
                                     'самые заветные желания. А такие ли они заветные'
                                     'или на самом деле навязанные? Зона видит вас насквозь...',
                         trailer='\'Stalker\' trailer link here',
                         year=1979,
                         rating=8.1,
                         genre_id=4,
                         director_id=5)
    test_movie_2 = Movie(id=2,
                         title='Дюна',
                         description='На пустынной планете аристократ Пол Атрейдес становится мессией'
                                     'и живой легендой. Мистический блокбастер Дэвида Линча,'
                                     'снятый по мотивам одноименного романа Фрэнка Герберта 1965 года.',
                         trailer='\'Dune\' trailer link here',
                         year=1984,
                         rating=6.3,
                         genre_id=7,
                         director_id=14)
    test_movie_3 = Movie(id=3,
                         title='Список Шиндлера',
                         description='История немецкого промышленника, спасшего тысячи жизней во время Холокоста.'
                                     'Драма Стивена Спилберга',
                         trailer='\"Schindler\'s List\" trailer link here',
                         year=1993,
                         rating=9.0,
                         genre_id=4,
                         director_id=3)

    movie_dao.get_all = MagicMock(return_value=[test_movie_1, test_movie_2, test_movie_3])
    movie_dao.get_one = MagicMock(return_value=test_movie_1)
    movie_dao.create = MagicMock(return_value=Movie(id=2))
    movie_dao.update = MagicMock()
    movie_dao.delete = MagicMock()
    return movie_dao


class TestMovieService:

    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_all(self):
        all_movies = self.movie_service.get_all()

        assert len(all_movies) > 0

    def test_get_one(self):
        single_movie = self.movie_service.get_one(2)

        assert single_movie is not None
        assert single_movie.id is not None

    def test_create(self):
        movie_data = {
            "title": "Дамасское время",
            "description": "Фильм рассказывает об иранском лётчике и его сыне, втором пилоте."
                           "Их самолёт был захвачен силами ISIS в Сирии, когда они доставляли"
                           "грузы гуманитарной помощи людям в зоне военных действий.",
            "trailer": "\'Be Vaghte Sham\' trailer link here",
            "year": 2018,
            "rating": 8.9,
            "genre_id": 6,
            "director_id": 12
        }

        new_movie = self.movie_service.create(movie_data)

        assert new_movie.id is not None

    def test_update(self):
        movie_data = {
            "title": "Прогулка по эшафоту",
            "description": "Двое влюбленных стали пленниками таинственного дома в глухом лесном уголке."
                           "Утром они проснулись и увидели павлина, а внутренности хижины возле эшафота"
                           "превратились в сказочные, роскошные чертоги..."
                           "Дмитрий Певцов в постсоветском философском хорроре",
            "trailer": "\'The walk on the scaffold\' trailer link here",
            "year": 1992,
            "rating": 6.7,
            "genre_id": 11,
            "director_id": 17
        }

        new_movie = self.movie_service.create(movie_data)

        assert new_movie.id is not None

    def test_delete(self):

        assert self.movie_service.delete(2) is None


if __name__ == "__main__":
    os.system("pytest -v")
