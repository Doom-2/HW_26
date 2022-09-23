import os
from unittest.mock import MagicMock
import pytest
from dao.models import Director
from dao.director import DirectorDAO
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)

    test_director_1 = Director(id=1, name='Андрей Тарковский')
    test_director_2 = Director(id=2, name='Дэвид Линч')
    test_director_3 = Director(id=3, name='Стивен Спилберг')

    director_dao.get_all = MagicMock(return_value=[test_director_1, test_director_2, test_director_3])
    director_dao.get_one = MagicMock(return_value=test_director_1)
    director_dao.create = MagicMock(return_value=Director(id=2))
    director_dao.update = MagicMock()
    director_dao.delete = MagicMock()
    return director_dao


class TestDirectorService:

    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_all(self):
        all_directors = self.director_service.get_all()

        assert len(all_directors) > 0

    def test_get_one(self):
        single_director = self.director_service.get_one(2)

        assert single_director is not None
        assert single_director.id is not None

    def test_create(self):
        director_data = {
            "name": "Эбрахим Хатамикия"
        }

        new_director = self.director_service.create(director_data)

        assert new_director.id is not None

    def test_update(self):
        director_data = {
            "name": "Исаак Фридберг"
        }

        new_director = self.director_service.create(director_data)

        assert new_director.id is not None

    def test_delete(self):
        assert self.director_service.delete(2) is None


if __name__ == "__main__":
    os.system("pytest")
