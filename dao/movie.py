from flask import request
from dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).get_or_404(mid)

    def get_all(self):
        return self.session.query(Movie).all()

    def get_all_paginate(self, page):
        return self.session.query(Movie).paginate(page, 5, error_out=False).items

    def get_by_filter(self):
        # Query values after '='
        director_id_query = request.args.get("director_id", type=int)
        genre_id_query = request.args.get("genre_id", type=int)
        year_query = request.args.get("year", type=int)

        if director_id_query:
            return self.session.query(Movie).filter(Movie.director_id == director_id_query)
        elif genre_id_query:
            return self.session.query(Movie).filter(Movie.genre_id == genre_id_query)
        elif year_query:
            return self.session.query(Movie).filter(Movie.year == year_query)

    def create(self, data):
        movie = Movie(**data)

        self.session.add(movie)
        self.session.commit()

        return movie

    def update(self, movie):

        self.session.add(movie)
        self.session.commit()

        return movie

    def delete(self, mid):
        movie = self.get_one(mid)

        self.session.delete(movie)
        self.session.commit()
