"""Web Routes."""

from masonite.routes import RouteGroup
from masonite.routes import Get, Post, Put, Delete

from app.http.controllers.CommentController import CommentController


ROUTES = [
    RouteGroup([
        # Authentication
        Post().route('/users/login', 'AuthController@login'),

        # User
        Post().route('/users', 'UserController@create'),
        Get().route('/user', 'UserController@currunt_user'),
        Put().route('/user', 'UserController@update'),

        # Profiles
        Get().route('/profiles/@username', 'ProfileController@show'),
        Post().route('/profiles/@username/follow', 'ProfileController@follow'),
        Delete().route('/profiles/@username/follow', 'ProfileController@unfollow'),

        # Articles
        Get().route('/articles', 'ArticleController@index'),
        Get().route('/articles/feed', 'ArticleController@feed'),
        Post().route('/articles', 'ArticleController@create'),
        Get().route('/articles/@slug', 'ArticleController@show'),
        Put().route('/articles/@slug', 'ArticleController@update'),
        Delete().route('/articles/@slug', 'ArticleController@delete'),
        Post().route('/articles/@slug/favorite', 'ArticleController@favorite'),
        Delete().route('/articles/@slug/favorite', 'ArticleController@unfavorite'),

        # Comments
        CommentController('/articles/@slug/comments').routes(),
    ], prefix='/api')
]
