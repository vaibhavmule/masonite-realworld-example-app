"""User Model."""
import jwt
import pendulum

from orator.orm import has_many

from config.database import Model
from config.application import KEY


class User(Model):
    """User Model."""

    __fillable__ = ['username', 'email', 'password', 'bio', 'image', 'token']

    __auth__ = 'email'
    __guarded__ = ['id', 'password']

    def generate_token(self):
        payload = {
            'issued': str(pendulum.now()),
            'expires': str(pendulum.now().add(minutes=1)),
            'refresh': str(pendulum.now().add(days=1)),
            'scopes' : ''
        }
        self.token = bytes(jwt.encode(payload, KEY, algorithm='HS256')).decode('utf-8')
        self.save()
        return self

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

    def favorite(self, article_id):
        from app.Favorite import Favorite
        Favorite.create({
            'user_id': self.id,
            'article_id': article_id
        })
