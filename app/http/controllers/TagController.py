""" A TagController Module """

from app.Tag import Tag


class TagController:
    """TagController."""

    def index(self):
        tags = Tag.lists('name')
        return {'tags': tags.serialize()}
