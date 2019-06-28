""" Tag Model """

from orator.orm import belongs_to_many

from config.database import Model


class Tag(Model):
    """Model Definition (generated with love by Masonite) 

    id: integer default: None
    name: string(255) default: None
    created_at: datetime default: CURRENT_TIMESTAMP
    updated_at: datetime default: CURRENT_TIMESTAMP
    """

    __fillable__ = ['name']

    @belongs_to_many
    def articles(self):
        from app.Article import Article
        return Article
