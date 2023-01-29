from flask import Flask, render_template, jsonify, Response
from flask_restx import Api
from flask_cors import CORS
from config import Config
from helpers.exceptions import BaseServiceError
from db_utils.setup_db import db
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.favotites import favorites_ns
from views.auth import auth_ns
from views.users import user_ns


def base_service_error_handler(exception: BaseServiceError):
    return jsonify({'error': str(exception)}), exception.code


def create_app(config: Config) -> Flask:
    application = Flask(__name__, template_folder="templates")
    application.config.from_object(config)
    application.url_map.strict_slashes = False
    application.app_context().push()

    @application.route('/')
    def index():
        return render_template('index.html')

    @application.route('/ping')
    def ping():
        return Response({'status': 'Ok'}, status=200)

    return application


def configure_app(application: Flask):
    CORS(app=app)
    db.init_app(application)
    api = Api(application, title="Flask Course Project 4", doc="/docs")
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(favorites_ns)
    app.register_error_handler(BaseServiceError, base_service_error_handler)


app_config = Config()
app = create_app(app_config)
configure_app(app)


if __name__ == '__main__':
    app.run(host="localhost", port=5000)
