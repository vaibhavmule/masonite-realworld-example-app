"""Web Routes."""

from masonite.routes import RouteGroup
from masonite.routes import Get, Post, Put

from app.resources.UserResource import UserResource

ROUTES = [
    UserResource('/api/users').routes(),
    Post().route('/api/users/login', 'AuthController@login'),
    Get().route('/api/user', 'AuthController@currunt_user'),
    Put().route('/api/user', 'AuthController@update'),
]
