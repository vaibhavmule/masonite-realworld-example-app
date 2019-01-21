""" Comment Model """

from orator.orm import belongs_to

from config.database import Model


class Comment(Model):
    """Comment Model."""

    __fillable__ = ['body', 'article_id', 'author_id']

    @belongs_to
    def article(self):
        from app.Article import Article
        return Article

    @belongs_to
    def author(self):
        from app.User import User
        return User
