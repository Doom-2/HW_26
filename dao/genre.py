from dao.models import Genre
from flask import current_app


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, genre_id):
        return self.session.query(Genre).get(genre_id)

    def get_all(self, page=None):
        if not page:
            return self.session.query(Genre).all()
        else:
            return self.session.query(Genre).paginate(
                page, current_app.config['ITEMS_PER_PAGE'],
                error_out=False
            ).items

    def create(self, data):
        genre = Genre(**data)

        self.session.add(genre)
        self.session.commit()

        return genre

    def update(self, genre):
        self.session.add(genre)
        self.session.commit()
        return genre

    def delete(self, genre_id):
        genre = self.get_one(genre_id)

        self.session.delete(genre)
        self.session.commit()
