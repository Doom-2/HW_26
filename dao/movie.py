from sqlalchemy import desc
from dao.models import Movie
from flask import current_app


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).get_or_404(mid)

    def get_all(self, page=None):
        if not page:
            return self.session.query(Movie).all()
        else:
            return self.session.query(Movie).paginate(
                page,
                current_app.config['ITEMS_PER_PAGE'],
                error_out=False
            ).items

    def get_by_filter(self, _filter=None, page=None):

        if _filter == 'new':
            filtered_movies = self.session.query(Movie).order_by(desc(Movie.year))
        else:
            filtered_movies = self.session.query(Movie).order_by(Movie.year)

        if page:
            return filtered_movies.paginate(
                page,
                current_app.config['ITEMS_PER_PAGE'],
                error_out=False
            ).items
        return filtered_movies

    def create(self, data):
        movie = Movie(**data)

        self.session.add(movie)
        self.session.commit()

        return movie

    def update(self, movie):

        self.session.add(movie)
        self.session.commit()

        return movie

    def get_favorites(self, user):
        user_favorite_movies = user.likes
        return user_favorite_movies

    def add_to_favorites(self, movie, user):
        user.likes.append(movie)
        self.session.commit()

    def delete_from_favorites(self, movie, user):
        user.likes.remove(movie)
        self.session.commit()

    def delete(self, mid):
        movie = self.get_one(mid)

        self.session.delete(movie)
        self.session.commit()
