import base64
import hashlib
import hmac
from dao.user import UserDAO
from flask import current_app


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):

        return self.dao.get_all()

    def get_one(self, uid):

        return self.dao.get_one(uid)

    def get_by_email(self, email):

        return self.dao.get_by_email(email)

    def create(self, user_data):
        user_data["password"] = self.get_hash(user_data.get("password"))

        return self.dao.create(user_data)

    def update_password(self, user_data):
        uid = user_data.get("id")
        user = self.dao.get_one(uid)
        user.password = self.get_hash(user_data.get("new_password"))
        self.dao.update(user)

        return self.dao

    def update_partial(self, user_data):
        uid = user_data.get("id")
        user = self.dao.get_one(uid)
        if "name" in user_data:
            user.name = user_data.get('name')
        if "surname" in user_data:
            user.surname = user_data.get('surname')
        if "favourite_genre" in user_data:
            user.favourite_genre_id = user_data.get('favourite_genre')
        self.dao.update(user)

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            current_app.config['PWD_HASH_SALT'],
            current_app.config['PWD_HASH_ITERATIONS']
        )

        return base64.b64encode(hash_digest)

    def compare_passwords(self, db_password_hash, password_from_request) -> bool:
        decoded_digest = base64.b64decode(db_password_hash)
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password_from_request.encode('utf-8'),
            current_app.config['PWD_HASH_SALT'],
            current_app.config['PWD_HASH_ITERATIONS']
        )

        return hmac.compare_digest(decoded_digest, hash_digest)
