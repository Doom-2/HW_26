from flask import request
from flask_restx import Resource, Namespace
from container import user_service, auth_service
from helpers.decorators import auth_required
from utils import bytes_to_dict
from dao.models import UserSchema

user_ns = Namespace('user')

user_schema = UserSchema()


@user_ns.route('/')
@user_ns.route('/password')
class UserView(Resource):
    @auth_required
    def get(self):
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user_instance = auth_service.get_user_by_token(token)
        return user_schema.dump(user_instance), 200

    @auth_required
    def put(self):
        request_data = bytes_to_dict(request.data)
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user_instance = auth_service.get_user_by_token(token)
        if not user_service.compare_passwords(user_instance.password, request_data['old_password']):
            return "Old password is wrong, try again", 401
        request_data["id"] = user_instance.id
        user_service.update_password(request_data)

        return "", 204

    @auth_required
    def patch(self):
        request_data = bytes_to_dict(request.data)
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user_instance = auth_service.get_user_by_token(token)
        request_data["id"] = user_instance.id
        user_service.update_partial(request_data)

        return "", 204
