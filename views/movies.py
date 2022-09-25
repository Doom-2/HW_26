from flask import request
from flask_restx import Resource, Namespace
from dao.models import MovieSchema
from container import movie_service
from helpers.decorators import auth_required
from helpers.parsers import page_parser

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    """
    The view contains requests to DB about all movies,
    divided by pages (pagination of 5 items per page).
    GET, POST http-methods are defined.
    """

    @auth_required
    @movie_ns.expect(page_parser)
    def get(self):

        all_movies = movie_service.get_all(**page_parser.parse_args())

        # key names in the request as list
        query_params = [i for i in request.args.keys()]
        status_query = request.args.get("status")

        try:
            if not query_params or 'page' in query_params and len(query_params) == 1:
                return movies_schema.dump(all_movies), 200
            else:
                only_new_movies = movie_service.get_new(status_query, **page_parser.parse_args())
                return movies_schema.dump(only_new_movies), 200
        except Exception as e:
            return str(e), 404

    def post(self):
        request_json = request.json
        new_movie = movie_service.create(request_json)
        return "", 201, {"location": f"/movies/{new_movie.id}"}


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    """
    The view contains requests to DB about single movie.
    GET, POST, PUT, PATCH, DELETE http-methods are defined.
    """

    @auth_required
    def get(self, mid: int):
        movie = movie_service.get_one(mid)
        return movie_schema.dump(movie), 200

    @auth_required
    def put(self, mid: int):
        request_json = request.json
        request_json["id"] = mid
        movie_service.update(request_json)
        return "", 204

    @auth_required
    def patch(self, mid: int):
        request_json = request.json
        request_json["id"] = mid
        movie_service.update_partial(request_json)
        return "", 204

    @auth_required
    def delete(self, mid: int):
        movie_service.delete(mid)
        return "", 204
