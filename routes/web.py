"""Web Routes."""

from masonite.routes import RouteGroup
from masonite.helpers.routes import get, post, put, delete


ROUTES = [
    RouteGroup([
        # Authentication
        post('/users/login', 'AuthController@login'),

        # User
        post('/users', 'UserController@create'),
        get('/user', 'UserController@currunt_user'),
        put('/user', 'UserController@update'),

        # Profiles
        get('/profiles/@username', 'ProfileController@show'),
        post('/profiles/@username/follow', 'ProfileController@follow'),
        delete('/profiles/@username/follow', 'ProfileController@unfollow'),

        # Articles
        get('/articles', 'ArticleController@index'),
        get('/articles/feed', 'ArticleController@feed'),
        post('/articles', 'ArticleController@create'),
        get('/articles/@slug', 'ArticleController@show'),
        put('/articles/@slug', 'ArticleController@update'),
        delete('/articles/@slug', 'ArticleController@delete'),
        post('/articles/@slug/favorite', 'ArticleController@favorite'),
        delete('/articles/@slug/favorite', 'ArticleController@unfavorite'),

        # Comments
        RouteGroup([
            get('/comments', 'CommentController@index'),
            post('/comments', 'CommentController@create'),
            delete('/comments/@id', 'CommentController@delete'),
        ], prefix='/articles/@slug'),

        # Tags
        get('/tags', 'TagController@index'),
    ], prefix='/api')
]
