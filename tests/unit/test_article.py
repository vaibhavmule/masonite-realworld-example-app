"""TestArticle Testcase."""

from masonite.testing import TestCase
from app.Article import Article
from app.User import User
from masonite.helpers import password


class TestArticle(TestCase):

    """All tests by default will run inside of a database transaction."""
    transactions = True

    def setUp(self):
        """Anytime you override the setUp method you must call the setUp method
        on the parent class like below.
        """
        super().setUp()

    def setUpFactories(self):
        """This runs when the test class first starts up.
        This does not run before every test case. Use this method to
        set your database up.
        """
        User.create({
            'username': 'Joe',
            'email': 'test@example.com',
            'password': password('secret'),
            'bio': 'This is a bio',
            'image': '',
            'token': None
        })

        Article.create({
            'title': 'this is a title',
            'slug': 'this-is-a-title',
            'description': 'This is a description',
            'body': 'this is a body',
            'author_id': 1
        })

    def test_can_create_article(self):
        self.assertTrue(self.get('/api/articles').hasJson('articlesCount', 1))

        self.actingAs(User.find(1)).json('POST', '/api/articles', {
                "article": {
                    "slug": "how-to-train-your-dragon",
                    "title": "How to train your dragon",
                    "description": "Ever wonder how?",
                    "body": "It takes a Jacobian",
                    "tagList": ["dragons", "training"],
                    "createdAt": "2016-02-18T03:22:56.637Z",
                    "updatedAt": "2016-02-18T03:48:35.824Z",
                    "favorited": False,
                    "favoritesCount": 0,
                    "author": {
                        "username": "jake",
                        "bio": "I work at statefarm",
                        "image": "https://i.stack.imgur.com/xHWG8.jpg",
                        "following": False
                    }
                }
        })

        self.assertTrue(Article.all().count())

    def test_article_can_update(self):
        article = Article.find(1)
        self.assertEqual(article.slug, 'this-is-a-title')
        self.assertEqual(article.tags.count(), 0)

        self.json('PUT', '/api/articles/this-is-a-title', {
            "article": {
                "slug": "this-is-another-slug",
                "title": "How to train your dragon",
                "description": "Dragons",
                "body": "I Love Dragons",
                "tagList": ['kids', 'adults']
            }
        })

        article = Article.find(1)
        self.assertEqual(article.slug, 'this-is-another-slug')
        self.assertEqual(article.tags.count(), 2)
    
    def test_article_can_be_deleted(self):
        Article.create({
            'title': 'delete this article',
            'slug': 'delete-this-article',
            'description': 'This is a description',
            'body': 'this is a body',
            'author_id': 1
        })

        article = Article.where('slug', 'delete-this-article').first()
        self.assertEqual(article.slug, 'delete-this-article')

        self.json('DELETE', '/api/articles/delete-this-article')

        article = Article.where('slug', 'delete-this-article').first()
        self.assertFalse(article)

    def test_can_index(self):
        self.assertTrue(
            self.json('GET', '/api/articles').hasAmount('articles', 2)
        )

    def test_can_show_single_json(self):
        Article.create({
            'title': 'this article',
            'slug': 'this-article',
            'description': 'This is a description',
            'body': 'this is a body',
            'author_id': 1
        })
        self.assertTrue(
            self.json('GET', '/api/articles/this-article').hasJson('article.slug', 'this-article')
        )
