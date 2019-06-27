"""Web Routes."""

from masonite.routes import RouteGroup, Get, Post, Put, Delete

ROUTES = [
    RouteGroup([
        # Authentication
        Post('/users/login', 'AuthController@login'),

        # User
        Post('/users', 'UserController@create'),
        Get('/user', 'UserController@current_user').middleware('auth'),
        Put('/user', 'UserController@update').middleware('auth'),

        # Profiles
        RouteGroup([
            Get('', 'ProfileController@show'),
            Post('follow', 'ProfileController@follow'),
            Delete('follow', 'ProfileController@unfollow'),
        ], middleware=('auth',), prefix='/profiles/@username'),

        # Articles
        Get('/articles', 'ArticleController@index'),
        Get('/articles/@slug', 'ArticleController@show'),

        RouteGroup([
            Post('', 'ArticleController@create'),
            Get('/feed', 'ArticleController@feed'),
            Put('/@slug', 'ArticleController@update'),
            Delete('/@slug', 'ArticleController@delete'),
            Post('/@slug/favorite', 'ArticleController@favorite'),
            Delete('/@slug/favorite', 'ArticleController@unfavorite'),
        ], prefix='/articles', middleware=('auth',)),

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
