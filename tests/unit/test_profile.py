"""TestProfile Testcase."""

from masonite.testing import TestCase
from app.User import User
from masonite.helpers import password


class TestProfile(TestCase):

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
            'username': 'Joe123',
            'email': 'Joe123@example.com',
            'password': password('secret')
        })
        User.create({
            'username': 'Bob123',
            'email': 'Bob123@example.com',
            'password': password('secret')
        })

    def test_can_get_profile(self):
        self.assertTrue(
            self.actingAs(User.find(1))
                .json('GET', '/api/profiles/Joe123').hasJson('profile.username', 'Joe123')
        )

    # def test_user_can_follow(self):
    #     self.assertTrue(
    #         self.actingAs(User.find(2))
    #             .json('POST', '/api/profiles/Joe123/follow').hasJson('profile.following', True)
    #     )

    # def test_user_can_unfollow(self):
    #     self.actingAs(User.find(2)).json('DELETE', '/api/profiles/Joe123/follow')

    #     self.assertTrue(
    #         self.actingAs(User.find(2))
    #             .json('POST', '/api/profiles/Joe123/follow').hasJson('profile.following', False)
    #     )
