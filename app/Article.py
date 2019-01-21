""" Article Model """

from orator.orm import belongs_to

from config.database import Model


class Article(Model):
    """Article Model"""
    __fillable__ = ['title', 'description', 'body', 'tagList']

    @belongs_to('author_id', 'id')
    def author(self):
        from app.User import User
        return User