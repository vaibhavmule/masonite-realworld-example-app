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

    def test_can_create_article(self):
        self.assertTrue(self.get('/api/articles').hasJson('articlesCount', 0))

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
