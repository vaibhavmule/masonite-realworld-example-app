from app.Tag import Tag


class TagController:

    def index(self):
        tags = Tag.lists('name').serialize()
        return {'tags': tags}
