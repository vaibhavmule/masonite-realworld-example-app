"""Web Routes."""

from masonite.routes import RouteGroup, Get, Post, Put, Delete

ROUTES = [
    RouteGroup([
        # Authentication
        Post('/users/login', 'AuthController@login'),

        # User
        Post('/users', 'UserController@create'),
        Get('/user', 'UserController@currunt_user'),
        Put('/user', 'UserController@update'),

        # Profiles
        Get('/profiles/@username', 'ProfileController@show'),
        Post('/profiles/@username/follow', 'ProfileController@follow'),
        Delete('/profiles/@username/follow', 'ProfileController@unfollow'),

        # Articles
        Get('/articles', 'ArticleController@index'),
        Get('/articles/feed', 'ArticleController@feed'),
        Post('/articles', 'ArticleController@create'),
        Get('/articles/@slug', 'ArticleController@show'),
        Put('/articles/@slug', 'ArticleController@update'),
        Delete('/articles/@slug', 'ArticleController@delete'),
        Post('/articles/@slug/favorite', 'ArticleController@favorite'),
        Delete('/articles/@slug/favorite', 'ArticleController@unfavorite'),

        # Comments
        RouteGroup([
            Get('/comments', 'CommentController@index'),
            Post('/comments', 'CommentController@create'),
            Delete('/comments/@id', 'CommentController@delete'),
        ], prefix='/articles/@slug'),

        # Tags
        Get('/tags', 'TagController@index'),
    ], prefix='/api')
]
