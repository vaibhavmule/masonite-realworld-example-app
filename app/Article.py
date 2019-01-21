""" Article Model """

from orator.orm import belongs_to, has_many

from app.Favorite import Favorite
from config.database import Model


class Article(Model):
    """Article Model"""
    __fillable__ = ['title', 'description', 'body', 'tagList']

    @belongs_to('author_id', 'id')
    def author(self):
        from app.User import User
        return User

    @has_many
    def comments(self):
        from app.Comment import Comment
        return Comment

    @has_many
    def favorites(self):
        from app.Favorite import Favorite
        return Favorite

    def is_favorite(self, user):
        if user:
            return bool(self.favorites.where('article_id', self.id).first())
        return False

    def paylaod(self, user):
        return {
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "body": self.body,
            "tagList": self.tagList.split(','),
            "createdAt": str(self.created_at),
            "updatedAt": str(self.updated_at),
            "favorited": self.is_favorite(user),
            "favoritesCount": self.favorites.count(),
            "author": {
                "username": self.author.username,
                "bio": self.author.bio,
                "image": self.author.image,
                "following": False
            }
        }
