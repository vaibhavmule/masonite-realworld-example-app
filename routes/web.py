"""Web Routes."""

from masonite.routes import RouteGroup
from masonite.routes import Get, Post, Put, Delete

from app.resources.UserResource import UserResource
from app.resources.CommentResource import CommentResource


ROUTES = [
    # Authentication
    UserResource('/api/users').routes(),
    Post().route('/api/users/login', 'AuthController@login'),
    Get().route('/api/user', 'AuthController@currunt_user'),
    Put().route('/api/user', 'AuthController@update'),

    # Profiles
    Get().route('/api/profiles/@username', 'ProfileController@show'),
    Post().route('/api/profiles/@username/follow', 'ProfileController@follow'),
    Delete().route('/api/profiles/@username/follow', 'ProfileController@unfollow'),

    # Articles
    Get().route('/api/articles', 'ArticleController@index'),
    Post().route('/api/articles', 'ArticleController@create'),
    Get().route('/api/articles/@slug', 'ArticleController@show'),
    Put().route('/api/articles/@slug', 'ArticleController@update'),
    Delete().route('/api/articles/@slug', 'ArticleController@delete'),
    Post().route('/api/articles/@slug/favorite', 'ArticleController@favorite'),
    Delete().route('/api/articles/@slug/favorite', 'ArticleController@unfavorite'),

    CommentResource('/api/articles/@slug/comments').routes(),
]
