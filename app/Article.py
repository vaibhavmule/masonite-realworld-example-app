"""Article Model."""

from orator.orm import belongs_to, has_many, belongs_to_many

from app.Favorite import Favorite
from config.database import Model


class Article(Model):
    """Model Definition (generated with love by Masonite).

    id: integer default: None
    slug: string(255) default: None
    title: string(255) default: None
    description: string(255) default: None
    body: text default: None
    author_id: integer default: None
    created_at: datetime default: CURRENT_TIMESTAMP
    updated_at: datetime default: CURRENT_TIMESTAMP
    """
    __fillable__ = ['title', 'description', 'body', 'slug', 'author_id']

    @belongs_to('author_id', 'id')
    def author(self):
        from app.User import User
        return User

    @belongs_to_many
    def tags(self):
        from app.Tag import Tag
        return Tag

    @has_many
    def comments(self):
        from app.Comment import Comment
        return Comment

    @has_many
    def favorites(self):
        from app.Favorite import Favorite
        return Favorite

    def save_tags(self, tags, type):
        from app.Tag import Tag
        tags = [
            Tag.first_or_create(name=name).id
            for name in tags
        ]
        
        if type == 'create':
            self.tags().attach(tags)
        
        if type == 'update':
            self.tags().sync(tags)

        return tags


    def is_favorite(self, user):
        if user:
            return bool(self.favorites.where('user_id', user.id).first())
        return False

    def payload(self, user):
        return {
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "body": self.body,
            "tagList": self.tags.lists('name'),
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
