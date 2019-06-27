"""Tag Model."""

from orator.orm import belongs_to_many

from config.database import Model


class Tag(Model):
    """Tag Model."""

    __fillable__ = ['name']

    @belongs_to_many
    def articles(self):
        from app.Article import Article
        return Article
