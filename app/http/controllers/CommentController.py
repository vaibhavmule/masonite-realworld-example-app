from masonite.request import Request

from app.Article import Article
from app.Comment import Comment
from app.Follow import Follow


class CommentController:

    def index(self, request: Request):
        article = Article.with_('comments.author').where(
            'slug', request.param('slug')).first()
        comments = [] 
        for comment in article.comments:
            comments.append(comment.payload())
        return {'comments': comments}

    def create(self, request: Request):
        article = Article.where('slug', request.param('slug')).first()
        comment = Comment(
            body=request.input('comment')['body'],
            author_id=request.user().id
        )
        article.comments().save(comment)
        return {'comment': comment.payload()}

    def delete(self, request: Request):
        comment = Comment.find(request.param('id'))
        if comment:
            comment.delete()
            return ''

        return {'error': 'Comment does not exist'}
