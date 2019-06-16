"""Web Routes."""

from masonite.routes import RouteGroup, Get, Post, Put, Delete

ROUTES = [
    RouteGroup([
        # Authentication
        Post('/users/login', 'AuthController@login'),

        # User
        Post('/users', 'UserController@create').middleware('auth'),
        Get('/user', 'UserController@currunt_user').middleware('auth'),
        Put('/user', 'UserController@update').middleware('auth'),

        # Profiles
        Get('/profiles/@username', 'ProfileController@show'),
        Post('/profiles/@username/follow', 'ProfileController@follow').middleware('auth'),
        Delete('/profiles/@username/follow', 'ProfileController@unfollow').middleware('auth'),

        # Articles
        Get('/articles', 'ArticleController@index'),
        Get('/articles/feed', 'ArticleController@feed').middleware('auth'),
        Post('/articles', 'ArticleController@create').middleware('auth'),
        Get('/articles/@slug', 'ArticleController@show'),
        Put('/articles/@slug', 'ArticleController@update').middleware('auth'),
        Delete('/articles/@slug', 'ArticleController@delete').middleware('auth'),
        Post('/articles/@slug/favorite', 'ArticleController@favorite').middleware('auth'),
        Delete('/articles/@slug/favorite', 'ArticleController@unfavorite').middleware('auth'),

        # Comments
        RouteGroup([
            Get('/comments', 'CommentController@index'),
            Post('/comments', 'CommentController@create').middleware('auth'),
            Delete('/comments/@id', 'CommentController@delete').middleware('auth'),
        ], prefix='/articles/@slug'),

        # Tags
        Get('/tags', 'TagController@index'),
    ], prefix='/api')
]
