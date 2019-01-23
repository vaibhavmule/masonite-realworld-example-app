"""User Model."""

from orator.orm import has_many

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

    @has_many('author_id')
    def articles(self):
        from app.Article import Article
        return Article

    @has_many
    def favorites(self):
        from app.Favorite import Favorite
        return Favorite

    @has_many('follower_id')
    def followed_users(self):
        from app.Follow import Follow
        return Follow
