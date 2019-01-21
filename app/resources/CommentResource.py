from api.resources import Resource
from api.serializers import JSONSerializer

from app.Article import Article
from app.Comment import Comment
from app.Follow import Follow


class CommentResource(Resource, JSONSerializer):
    model = Comment
    methods = ['index', 'create', 'delete']

    def index(self):
        article = Article.where('slug', self.request.param('slug')).first()
        comments = self.model.where('article_id', article.id).get()
        
        payload = [] 

        for comment in comments:
            payload.append({
                "id": comment.id,
                "createdAt": str(comment.created_at),
                "updatedAt": str(comment.updated_at),
                "body": comment.body,
                "author": {
                    "username": article.author.username,
                    "bio": article.author.bio,
                    "image": article.author.image,
                    "following": False
                }
            })
        return {'comments': payload}

    def create(self):
        article = Article.where('slug', self.request.param('slug')).first()
        comment = self.model.create(
            body=self.request.input('comment')['body'],
            article_id=article.id,
            author_id=self.request.user().id
        )
        payload = {
            "id": comment.id,
            "createdAt": str(comment.created_at),
            "updatedAt": str(comment.updated_at),
            "body": comment.body,
            "author": {
                "username": article.author.username,
                "bio": article.author.bio,
                "image": article.author.image,
                "following": False
            }
        }
        return {'comment': payload}