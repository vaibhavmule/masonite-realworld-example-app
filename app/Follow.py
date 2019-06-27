"""Follow Model"""

from orator.orm import belongs_to

from config.database import Model

class Follow(Model):
    """Follow Model."""

    __fillable__ = ['user_id', 'follower_id']

    @belongs_to('user_id', 'id')
    def user(self):
        from app.User import User
        return User

    @belongs_to('follower_id', 'id')
    def follower(self):
        from app.User import User
        return User