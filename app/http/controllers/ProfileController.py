from masonite.request import Request

from app.User import User
from app.Follow import Follow

class ProfileController:

    def show(self, request: Request):
        user = User.where('username', request.param('username')).first()
        return {'profile': user.payload(request.user())}

    def follow(self, request: Request):
        user = User.where('username', request.param('username')).first()
        follow = Follow.first_or_create(
            user_id=user.id,
            follower_id=request.user().id
        )
        return {'profile': user.payload(request.user(), follow)}
    
    def unfollow(self, request: Request):
        user = User.where('username', request.param('username')).first()
        follow = Follow.where('user_id', user.id).where('follower_id', request.user().id).first()
        if follow:
            follow.delete()
        return {'profile': user.payload(request.user())}
