import json 

from masonite.request import Request
from masonite.validation import Validator

from slugify import slugify

from app.Article import Article
from app.Favorite import Favorite
from app.Tag import Tag
from app.User import User


class ArticleController:

    def __init__(self, request: Request):
        self.request = request
        self.user = request.user()

    def index(self):
        articles = Article.with_('author', 'favorites')

        if self.request.has('author'):
            user = User.where('username', self.request.input('author')).first()

            if user:
                articles.where('author_id', user.id)

        if self.request.has('favorited'):
            user = User.where('username', self.request.input('favorited')).first()
            
            if user:
                articles.where_in('id', user.favorites.pluck('article_id'))

        if self.request.has('tag'):
            tag = Tag.where('name', self.request.input('tag')).first()
            
            if tag:
                articles.where_in('id', tag.articles.pluck('id'))

        articles = articles.order_by('created_at', 'desc').paginate(
            self.request.input('limit', 20),
            self.request.input('offset', 0)
        )

        list_of_articles = [article.payload(self.request.user()) for article in articles]
        return {'articles': list_of_articles, 'articlesCount': articles.count()}

    def feed(self):
        users = self.user.followed_users().lists('user_id').serialize()
        articles = Article.with_('author', 'favorites').where_in('author_id', users)
        if articles:
            articles = articles.order_by('created_at', 'desc').paginate(
                self.request.input('limit'),
                self.request.input('offset')
            )
        list_of_articles = [article.payload(self.user) for article in articles]
        return {'articles': list_of_articles, 'articlesCount': len(list_of_articles)}

    def show(self, slug):
        article = Article.with_('author').where('slug', slug).first()
        return {'article': article.payload(self.request.user())}

    def create(self, validator: Validator, validate: Validator):
        article_data = self.request.input('article')

        errors = self.request.validate(
            validate.required(['article.title', 'article.description', 'article.body']),
        )
        if errors:
            self.request.status(422)
            return {'errors': errors}
        
        article = Article()
        article.slug=slugify(article_data['title'])
        article.title=article_data['title']
        article.description=article_data['description']
        article.body=article_data['body']
        article.author_id = self.request.user().id
        article.save()

        article.save_tags(self.request.input('article')['tagList'], 'create')
        
        article = Article.with_('author', 'tags').find(article.id)
        self.request.status(201)
        return {'article': article.payload(self.request.user())}

    def update(self, slug):
        article = Article.with_('author').where('slug', slug).first()
        article.update(self.request.input('article'))
        if self.request.input('article.tagList'):
            article.save_tags(self.request.input('article.tagList'), 'update')

        return {'article': article.payload(self.request.user())}

    def delete(self, slug):
        article = Article.where('slug', slug).first()
        if article:
            article.tags().detach(article.tags.lists('id'))
            article.delete()
            return self.request.status(204)

        return {'error': 'Article does not exist'}

    def favorite(self, slug):
        article = Article.where('slug', slug).first()
        favorite = Favorite(
            user_id=self.request.user().id
        )
        article.favorites().save(favorite)
        article = Article.with_('author', 'favorites').where('slug', slug).first()
        return {'article': article.payload(self.request.user())}

    def unfavorite(self, slug):
        article = Article.where('slug', slug).first()
        if article:
            favorite = article.favorites.where('user_id', self.request.user().id).first()
            favorite.delete()
        article = Article.with_('author', 'favorites').where('slug', self.request.param('slug')).first()
        return {'article': article.payload(self.request.user())}
