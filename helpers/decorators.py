import jwt
from flask import request, current_app
from flask_restx import abort


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]

        try:
            jwt.decode(
                token,
                current_app.config['JWT_SECRET'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


# not used in this project
def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        role = None

        try:
            user = jwt.decode(
                token,
                current_app.config['JWT_SECRET'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            role = user.get("role", "user")
        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)

        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper
