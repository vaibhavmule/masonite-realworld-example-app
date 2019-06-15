import json 

from masonite.request import Request
from masonite.validation import Validator

from slugify import slugify

from app.Article import Article
from app.Favorite import Favorite
from app.Tag import Tag
from app.User import User


class ArticleController:

    def index(self, request: Request):
        articles = Article.with_('author', 'favorites')
        user = User.where(
            'username', request.input('author', '') or request.input('favorited', '')).first()
        tag = Tag.where('name', request.input('tag', '')).first()

        if request.input('author'):
            try:
                articles = user.articles().with_('author', 'favorites')
            except:
                articles = []

        if request.input('favorited'):
            try:
                article_ids = user.favorites().lists('article_id').serialize()
            except:
                article_ids = []
        
            articles = articles.where_in('id', article_ids)

        if request.input('tag'):
            try:
                article_ids = tag.articles().lists('article_id').serialize()
            except:
                article_ids = []
            articles = articles.where_in('id', article_ids)

        if articles:
            articles = articles.order_by('created_at', 'desc').paginate(
                request.input('limit'),
                request.input('offset')
            )
        print(articles)
        list_of_articles = [article.paylaod(request.user()) for article in articles]
        return {'articles': list_of_articles, 'articlesCount': len(list_of_articles)}

    def feed(self, request: Request):
        users = request.user().followed_users().lists('user_id').serialize()
        articles = Article.with_('author', 'favorites').where_in('author_id', users)
        if articles:
            articles = articles.order_by('created_at', 'desc').paginate(
                request.input('limit'),
                request.input('offset')
            )
        list_of_articles = [article.paylaod(request.user()) for article in articles]
        return {'articles': list_of_articles, 'articlesCount': len(list_of_articles)}

    def show(self, request: Request):
        article = Article.with_('author').where('slug', request.param('slug')).first()
        return {'article': article.paylaod(request.user())}

    def create(self, request: Request, validator: Validator, validate: Validator):
        article_data = request.input('article')

        errors = validator.validate(
            article_data,
            validate.required(['title', 'description', 'body']),
        )
        if errors:
            request.status(422)
            return {'errors': errors}
        
        article = Article()
        article.slug=slugify(article_data['title'])
        article.title=article_data['title']
        article.description=article_data['description']
        article.body=article_data['body']
        article.author_id=request.user().id
        article.save()

        article.save_tags(request.input('article')['tagList'], 'create')
        
        article = Article.with_('author', 'tags').find(article.id)
        request.status(201)
        return {'article': article.paylaod(request.user())}

    def update(self, request: Request):
        article = Article.with_('author').where('slug', request.param('slug')).first()
        article.update(request.input('article'))
        if 'tagList' in request.input('article'):
            article.save_tags(request.input('article')['tagList'], 'update')
        return {'article': article.paylaod(request.user())}

    def delete(self, request: Request):
        article = Article.where('slug', request.param('slug')).first()
        if article:
            article.tags().detach(article.tags.lists('id'))
            article.delete()
            return request.status(204)

        return {'error': 'Article does not exist'}

    def favorite(self, request: Request):
        article = Article.where('slug', request.param('slug')).first()
        favorite = Favorite(
            user_id=request.user().id
        )
        article.favorites().save(favorite)
        article = Article.with_('author', 'favorites').where('slug', request.param('slug')).first()
        return {'article': article.paylaod(request.user())}

    def unfavorite(self, request: Request):
        article = Article.where('slug', request.param('slug')).first()
        if article:
            favorite = article.favorites.where('user_id', request.user().id).first()
            favorite.delete()
        article = Article.with_('author', 'favorites').where('slug', request.param('slug')).first()
        return {'article': article.paylaod(request.user())}
