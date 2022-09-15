from flask import request
from flask_restx import Resource, Namespace
from dao.model.director import DirectorSchema
from container import director_service
from helpers.decorators import auth_required, admin_required

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):

    @auth_required
    def get(self):
        all_directors = director_service.get_all()
        response = directors_schema.dump(all_directors)
        return response, 200

    @admin_required
    def post(self):
        request_json = request.json
        new_director = director_service.create(request_json)
        return "", 201, {"location": f"/directors/{new_director.id}"}


@director_ns.route('/<int:dir_id>')
class DirectorView(Resource):

    @auth_required
    def get(self, dir_id):
        single_director = director_service.get_one(dir_id)
        response = director_service.dump(single_director)
        return response, 200

    @admin_required
    def put(self, dir_id: int):
        request_json = request.json
        request_json["id"] = dir_id
        director_service.update(request_json)
        return "", 204

    @admin_required
    def delete(self, dir_id: int):
        director_service.delete(dir_id)
        return "", 204
