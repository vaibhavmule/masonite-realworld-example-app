from masonite.testing import TestCase
from app.Article import Article
from app.User import User
from masonite.helpers import password

class TestUser(TestCase):

    def setUp(self):
        super().setUp()
    
    def setUpFactories(self):
        User.create({
            'email': 'joe@example.com',
            'password': password('secret'),
            'username': 'Joe'
        })
    
    def test_user_can_login(self):
        self.assertTrue(self.json('POST', '/api/users/login', {
            'user': {
                'email': 'joe@example.com',
                'password': 'secret'
            }
        }).contains('user'))

    def test_user_cant_login_with_wrong_credentials(self):
        self.assertTrue(self.json('POST', '/api/users/login', {
            'user': {
                'email': 'joe@example.com',
                'password': 'nosecert'
            }
        }).contains('error'))

    def test_user_can_be_created(self):
        self.assertTrue(
            self.json('POST', '/api/users', {
                'user': {
                    'email': 'bob@example.com',
                    'password': password('secret'),
                    'username': 'Bob'
                }
            }).hasJson('user.email', 'bob@example.com')
        )

    def test_user_can_be_updated(self):
        self.assertTrue(
            self.actingAs(User.find(1)).json('PUT', '/api/user', {
                'user': {
                    'email': 'John@example.com',
                    'password': password('secret'),
                    'username': 'John'
                }
            }).hasJson('user.email', 'John@example.com')
        )

