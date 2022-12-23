# Movies-4-U
### Netflix analogue with users support.
### Containerized with Docker, running on Gunicorn. CI/CD integration is used

[movies-4-u.ga](http://movies-4-u.ga)

#### Features:
- User authentication with jwt
- User profile, including password change ability
- Favorites page
- Filtering movies by director and genre

#### Details:
- models based on ORM Flask SQLAlchemy
- marshmallow serialization
- PostgreSQL integration
- endpoints aggregated using Namespaces
- REST for movies, directors, genres, users
- architecture based on DAO & Service layers
- content availability via authentication
- jwt token validation using decorators 
- filtering movies with query string
- favorites table based on Many-To-Many Relationship
- unit tests for DAO, services and views using
- using the MagicMock method and pytest fixtures

![Movies-4-U.gif](static%2Fimg%2FMovies-4-U.gif)