from dao.models import Director
from flask import current_app


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, dir_id):
        return self.session.query(Director).get(dir_id)

    def get_all(self, page=None):
        if not page:
            return self.session.query(Director).all()
        else:
            return self.session.query(Director).paginate(
                page,
                current_app.config['ITEMS_PER_PAGE'],
                error_out=False
            ).items

    def create(self, data):
        director = Director(**data)

        self.session.add(director)
        self.session.commit()

        return director

    def update(self, director):
        self.session.add(director)
        self.session.commit()
        return director

    def delete(self, dir_id):
        director = self.get_one(dir_id)

        self.session.delete(director)
        self.session.commit()
