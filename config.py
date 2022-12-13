import base64
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env', raise_error_if_not_found=False))


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'.format(
        username=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST', '127.0.0.1'),
        port=int(os.getenv('POSTGRES_PORT', 5432)),
        db_name=os.getenv('POSTGRES_DB')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_EXPIRE_MINUTES = 15
    TOKEN_EXPIRE_DAYS = 130

    PWD_HASH_SALT = base64.b64decode("salt")
    PWD_HASH_ITERATIONS = 100_000

    JWT_ALGORITHM = 'HS256'
    JWT_SECRET = 's3cR$eT'

    ITEMS_PER_PAGE = 12