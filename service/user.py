import base64
import hashlib
import hmac
from dao.user import UserDAO
from helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create(self, user_data):
        user_data["password"] = self.get_hash(user_data.get("password"))
        return self.dao.create(user_data)

    def update(self, user_data):
        user_data["password"] = self.get_hash(user_data.get("password"))
        self.dao.update(user_data)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def compare_passwords(self, db_password_hash, password_from_request) -> bool:
        decoded_digest = base64.b64decode(db_password_hash)
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password_from_request.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decoded_digest, hash_digest)
