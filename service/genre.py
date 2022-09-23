from dao.genre import GenreDAO
from helpers.exceptions import ItemNotFound


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_all(self, page=None):
        return self.dao.get_all(page)

    def get_one(self, genre_id):
        if genre := self.dao.get_one(genre_id):
            return genre
        raise ItemNotFound(f'Genre with pk={genre_id} not exists.')

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        genre_id = data.get("id")
        genre = self.dao.get_one(genre_id)
        genre.name = data.get('name')

        self.dao.update(data)

    def delete(self, genre_id):
        self.dao.delete(genre_id)
