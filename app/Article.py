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