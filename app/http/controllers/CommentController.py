from masonite.request import Request

from masonite.validation import Validator

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

    def create(self, request: Request, validator: Validator, validate: Validator):
        comment_data = request.input('comment')

        errors = validator.validate(
            comment_data,
            validate.required(['body']),
        )
        if errors:
            request.status(422)
            return {'errors': errors}
        article = Article.where('slug', request.param('slug')).first()
        comment = Comment(
            body=comment_data['body'],
            author_id=request.user().id
        )
        article.comments().save(comment)
        request.status(201)
        return {'comment': comment.payload()}

    def delete(self, request: Request):
        comment = Comment.find(request.param('id'))
        if comment:
            comment.delete()
            return request.status(204)

        return {'error': 'Comment does not exist'}
