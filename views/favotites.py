from flask import request
from flask_restx import Resource, Namespace
from container import auth_service, movie_service
from helpers.decorators import auth_required
from dao.models import MovieSchema

favorites_ns = Namespace('favorites')
movies_schema = MovieSchema(many=True)


@favorites_ns.route('/movies')
class FavoritesView(Resource):

    @auth_required
    def get(self):
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user_instance = auth_service.get_user_by_token(token)
        user_favorites_movies = movie_service.get_favorites(user_instance)
        return movies_schema.dump(user_favorites_movies), 200


@favorites_ns.route('/movies/<int:mid>')
class FavoriteView(Resource):
    @auth_required
    def post(self, mid):
        selected_movie = movie_service.get_one(mid)
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user_instance = auth_service.get_user_by_token(token)
        movie_service.add_to_favorites(selected_movie, user_instance)
        return "", 201, {"location": f"/favorites/movies/{mid}"}

    @auth_required
    def delete(self, mid):
        selected_movie = movie_service.get_one(mid)
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user_instance = auth_service.get_user_by_token(token)
        movie_service.delete_from_favorites(selected_movie, user_instance)
        return "", 204
