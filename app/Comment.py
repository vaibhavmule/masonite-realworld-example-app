"""Comment Model."""

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

    def payload(self):
        return {
            "id": self.id,
            "createdAt": str(self.created_at),
            "updatedAt": str(self.updated_at),
            "body": self.body,
            "author": {
                "username": self.author.username,
                "bio": self.author.bio,
                "image": self.author.image,
                "following": False
            }
        }
