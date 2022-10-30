import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from app import app
from db_utils.setup_db import db

if __name__ == '__main__':
    def create_data():
        with app.app_context():
            db.drop_all()
            db.create_all()

    create_data()
