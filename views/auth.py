from flask import request
from flask_restx import Namespace, Resource
from container import auth_service, user_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class RegisterView(Resource):
    """
    Create a user
    """

    def post(self):
        request_json = request.json
        new_user = user_service.create(request_json)
        return "", 201, {"location": f"{new_user.id}"}


@auth_ns.route('/login')
class LoginView(Resource):
    """
    Authenticate a user
    """

    def post(self):
        data = request.json

        # If there are no 'email' or 'password' fields
        # in POST-request body, returns 400
        email = data.get("email", None)
        password = data.get("password", None)
        if None in [email, password]:
            return "", 400

        tokens = auth_service.generate_tokens(email, password)
        return tokens, 201

    def put(self):
        data = request.json
        refresh_token = data.get("refresh_token")

        tokens = auth_service.approve_refresh_token(refresh_token)
        return tokens, 201
