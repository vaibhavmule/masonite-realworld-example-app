""" Favorite Model """

from orator.orm import belongs_to

from config.database import Model


class Favorite(Model):
    """Favorite Model."""

    __fillable__ = ['user_id', 'article_id']

    @belongs_to('user_id', 'id')
    def user(self):
        from app.User import User
        return User

    @belongs_to('article_id', 'id')
    def article(self):
        from app.Article import Article
        return Article
