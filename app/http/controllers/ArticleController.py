""" A ArticleController Module """
import json 

from masonite.request import Request

from slugify import slugify

from app.Article import Article
from app.Favorite import Favorite
from app.User import User

from config.database import DB


class ArticleController:
    """ArticleController"""

    def index(self, request: Request):
        articles = []
        author = User.where('username', request.input('author', '')).first()
        if author:
            articles = Article.with_('author', 'favorites').where('author_id', author.id).get()

        list_of_articles = []
        for article in articles:
            list_of_articles.append(article.paylaod(request.user()))
        return {'articles': list_of_articles,'articlesCount': len(list_of_articles)}

    def feed(self, request: Request):
        pass

    def show(self, request: Request):
        article = Article.with_('author').where('slug', request.param('slug')).first()
        return {'article': article.paylaod(request.user())}

    def create(self, request: Request):
        article_data = request.input('article')
        article = Article()
        article.slug=slugify(article_data['title'])
        article.title=article_data['title']
        article.description=article_data['description']
        article.body=article_data['body']
        article.tagList= ','.join(article_data['tagList'])
        article.author_id=request.user().id
        article.save()

        article = Article.with_('author').find(article.id)
        return {'article': article.paylaod(request.user())}

    def update(self, request: Request):
        article = Article.with_('author').where('slug', request.param('slug')).first()
        article.update(request.input('article'))
        return {'article': article.paylaod(request.user())}

    def delete(self, request: Request):
        article = Article.where('slug', request.param('slug')).first()
        if article:
            article.delete()
            return ''

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
