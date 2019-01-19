""" A ProfileController Module """
from masonite.request import Request

from app.User import User
from app.Follow import Follow

class ProfileController:
    """ProfileController
    """

    def show(self, request: Request):
        user = User.where('username', request.param('username')).first()
        follow = Follow.where('user_id', user.id).where('follower_id', request.user().id).first()
        profile = { 
            'username': user.username,
            'image': user.image,
            'bio': user.bio,
            'following': True if follow else False
        }
        return {'profile': profile}

    def follow(self, request: Request):
        user = User.where('username', request.param('username')).first()
        follow = Follow.first_or_create(
            user_id=user.id,
            follower_id=request.user().id
        )
        profile = {
            'username': user.username,
            'image': user.image,
            'bio': user.bio,
            'following': True if follow else False
        }
        return {'profile': profile}
    
    def unfollow(self, request: Request):
        user = User.where('username', request.param('username')).first()
        follow = Follow.where('user_id', user.id).where('follower_id', request.user().id).first()
        follow.delete()
        profile = {
            'username': user.username,
            'image': user.image,
            'bio': user.bio,
            'following': False
        }
        return {'profile': profile}