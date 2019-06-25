from app.Tag import Tag


class TagController:

    def index(self):
        tags = Tag.lists('name')
        return {'tags': tags.serialize()}
