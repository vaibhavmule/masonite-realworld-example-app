"""Authentication Middleware."""

from masonite.request import Request
from masonite.response import Response

class AuthenticationMiddleware:
    """Middleware To Check If The User Is Logged In."""

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    def before(self):
        if not self.request.user():
            return self.response.json({'errors': 'Unauthorized request'}, status=401)

    def after(self):
        pass
