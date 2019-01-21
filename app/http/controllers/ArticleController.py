""" A ArticleController Module """
import json 

from masonite.request import Request

from slugify import slugify

from app.Article import Article
from app.User import User

from config.database import DB


class ArticleController:
    """ArticleController
    """

    def index(self, request: Request):
        articles = []
        author = User.where('username', request.input('author', '')).first()
        if author:
            articles = Article.where('author_id', author.id).get()

        list_of_articles = []
        for article in articles:
            list_of_articles.append({
                "slug": article.slug,
                "title": article.title,
                "description": article.description,
                "body": article.body,
                "tagList": article.tagList,
                "createdAt": str(article.created_at),
                "updatedAt": str(article.updated_at),
                "favorited": False,
                "favoritesCount": 0,
                "author": {
                    "username": article.author.username,
                    "bio": article.author.bio,
                    "image": article.author.image,
                    "following": False
                }
            })
        return {'articles': list_of_articles,'articlesCount': len(list_of_articles) }

    def show(self, request: Request):
        article = Article.where('slug', request.param('slug')).first()
        payload = {
            "slug": article.slug,
            "title": article.title,
            "description": article.description,
            "body": article.body,
            "tagList": article.tagList.split(','),
            "createdAt": str(article.created_at),
            "updatedAt": str(article.updated_at),
            "favorited": False,
            "favoritesCount": 0,
            "author": {
                "username": article.author.username,
                "bio": article.author.bio,
                "image": article.author.image,
                "following": False
            }
        }   
        return {'article': payload}

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

        article = Article.find(article.id)
        payload = {
            "slug": article.slug,
            "title": article.title,
            "description": article.description,
            "body": article.body,
            "tagList": article.tagList.split(','),
            "createdAt": str(article.created_at),
            "updatedAt": str(article.updated_at),
            "favorited": False,
            "favoritesCount": 0,
            "author": {
                "username": article.author.username,
                "bio": article.author.bio,
                "image": article.author.image,
                "following": False
            }
        }   
        return {'article': payload}

    def update(self, request: Request):
        article = Article.where('slug', request.param('slug')).first()
        article.update(request.input('article'))
        article = Article.find(article.id)
        payload = {
            "slug": article.slug,
            "title": article.title,
            "description": article.description,
            "body": article.body,
            "tagList": article.tagList.split(','),
            "createdAt": str(article.created_at),
            "updatedAt": str(article.updated_at),
            "favorited": False,
            "favoritesCount": 0,
            "author": {
                "username": article.author.username,
                "bio": article.author.bio,
                "image": article.author.image,
                "following": False
            }
        }   
        return {'article': payload}

    def delete(self, request: Request):
        article = Article.where('slug', request.param('slug')).first()
        if article:
            article.delete()
            request.status()
        return ''
