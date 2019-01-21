from api.resources import Resource
from api.serializers import JSONSerializer

from app.Article import Article
from app.Comment import Comment
from app.Follow import Follow


class CommentController(Resource, JSONSerializer):
    model = Comment
    methods = ['index', 'create', 'delete']

    def index(self):
        article = Article.with_('comments.author').where(
            'slug', self.request.param('slug')).first()
        comments = [] 
        for comment in article.comments:
            comments.append(comment.payload())
        return {'comment': comments}

    def create(self):
        article = Article.where('slug', self.request.param('slug')).first()
        comment = self.model(
            body=self.request.input('comment')['body'],
            author_id=self.request.user().id
        )
        article.comments().save(comment)
        return {'comment': comment.payload()}
