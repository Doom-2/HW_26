from app import app
from db_utils.setup_db import db

if __name__ == '__main__':
    def create_data():
        with app.app_context():
            db.create_all()

    create_data()
