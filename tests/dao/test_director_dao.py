from dao.models import Director
from unittest.mock import MagicMock
import pytest
import os


def get_all(page=None):
    if not page:
        return Director.query.all()
    else:
        return Director.query.paginate(page, 12, error_out=False).items


def get_one(dir_id):
    return Director.query.get(dir_id)


def create(director_data):
    new_director = Director.add(director_data)
    return new_director


@pytest.fixture()
def director_objects():
    dir1 = Director(id=1, name='Владимир Вайншток')
    dir2 = Director(id=2, name='Стэнли Кубрик')
    dir3 = Director(id=3, name='Ричард Келли')
    return {1: dir1, 2: dir2, 3: dir3}


@pytest.fixture
def director(director_objects):
    director_instance = Director
    director_instance.query = MagicMock()
    director_instance.query.all = MagicMock(return_value=director_objects.values())
    director_instance.query.get = MagicMock(side_effect=director_objects.get)
    director_instance.add = MagicMock(return_value=Director(id=2))
    return director_instance


def test_get_all(director):
    all_directors = get_all()
    assert len(all_directors) > 0


def test_get_one(director):
    single_director = get_one(2)
    expected = "Стэнли Кубрик"
    assert single_director.name == expected


def test_create(director):
    director_data = {
        "name": "Эбрахим Хатамикия"
    }
    new_director = create(director_data)
    assert new_director.id == 2


if __name__ == "__main__":
    os.system("pytest")
