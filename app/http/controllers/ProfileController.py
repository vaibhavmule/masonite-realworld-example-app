from masonite.request import Request

from app.User import User
from app.Follow import Follow

class ProfileController:

    def __init__(self, request: Request):
        self.request = request
        self.user = request.user()

    def show(self, username):
        user = User.where('username', username).first()
        return {'profile': user.payload(self.user)}

    def follow(self, username):
        user = User.where('username', username).first()
        follow = Follow.first_or_create(
            user_id=user.id,
            follower_id=self.user.id
        )
        return {'profile': user.payload(self.user, follow)}
    
    def unfollow(self, username):
        user = User.where('username', username).first()
        Follow.where('user_id', user.id).where('follower_id', self.user.id).delete()
        return {'profile': user.payload(self.user)}
