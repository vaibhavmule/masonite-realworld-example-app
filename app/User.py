"""User Model."""

from config.database import Model


class User(Model):
    """User Model."""

    __fillable__ = ['username', 'email', 'password', 'bio', 'image', 'token']

    __auth__ = 'email'
    __guarded__ = ['id', 'password']

    def payload(self, user, follow=False):
        from app.Follow import Follow
        if not follow:
            follow = Follow.where('user_id', self.id).where('follower_id', user.id).first()
        return {
            'username': self.username,
            'image': self.image,
            'bio': self.bio,
            'following': bool(follow)
        }
