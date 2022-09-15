from flask import request
from flask_restx import Resource, Namespace
from container import user_service
from dao.model.user import UserSchema

user_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all()
        response = users_schema.dump(all_users)
        return response, 200

    def post(self):
        request_json = request.json
        new_user = user_service.create(request_json)
        return "", 201, {"location": f"{new_user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        single_user = user_service.get_one(uid)
        response = user_schema.dump(single_user)
        return response, 200

    def put(self, uid: int):
        request_json = request.json
        request_json["id"] = uid
        user_service.update(request_json)
        return "", 204

    def delete(self, uid: int):
        user_service.delete(uid)
        return "", 204
