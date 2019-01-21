""" Article Model """

from orator.orm import belongs_to

from app.Favorite import Favorite
from config.database import Model


class Article(Model):
    """Article Model"""
    __fillable__ = ['title', 'description', 'body', 'tagList']

    @belongs_to('author_id', 'id')
    def author(self):
        from app.User import User
        return User

    def favorite_count(self):
        return Favorite.where('article_id', self.id).count()

    def paylaod(self, user, favorite=None):
        if not favorite and user:
            favorite = Favorite.where('user_id', user.id).where(
                'article_id', self.id).first()
        return {
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "body": self.body,
            "tagList": self.tagList.split(','),
            "createdAt": str(self.created_at),
            "updatedAt": str(self.updated_at),
            "favorited": True if favorite else False,
            "favoritesCount": self.favorite_count(),
            "author": {
                "username": self.author.username,
                "bio": self.author.bio,
                "image": self.author.image,
                "following": False
            }
        }
