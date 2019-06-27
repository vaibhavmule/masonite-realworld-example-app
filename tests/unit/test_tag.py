"""TestTag Testcase."""

from masonite.testing import TestCase


class TestTag(TestCase):

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
        pass

    def test_can_get_tags(self):
        self.assertTrue(
            self.json('GET', '/api/tags').hasJson({
                'tags': []})
        )
