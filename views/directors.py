from flask import request
from flask_restx import Resource, Namespace
from dao.models import DirectorSchema
from container import director_service
from helpers.decorators import auth_required
from helpers.parsers import page_parser

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):

    @auth_required
    @director_ns.expect(page_parser)
    def get(self):
        all_directors = director_service.get_all(**page_parser.parse_args())
        response = directors_schema.dump(all_directors)
        return response, 200

    def post(self):
        request_json = request.json
        new_director = director_service.create(request_json)
        return "", 201, {"location": f"/directors/{new_director.id}"}


@director_ns.route('/<int:dir_id>')
class DirectorView(Resource):

    @auth_required
    def get(self, dir_id):
        single_director = director_service.get_one(dir_id)
        response = director_schema.dump(single_director)
        return response, 200

    @auth_required
    def put(self, dir_id: int):
        request_json = request.json
        request_json["id"] = dir_id
        director_service.update(request_json)
        return "", 204

    @auth_required
    def delete(self, dir_id: int):
        director_service.delete(dir_id)
        return "", 204
