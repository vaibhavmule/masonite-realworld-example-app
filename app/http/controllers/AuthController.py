"""A AuthController Module"""

from masonite.auth import Auth
from masonite.request import Request

from app.User import User


class AuthController:
    """AuthController."""

    def login(self, request: Request, auth: Auth):
        user_data = request.input('user')
        if auth.once().login(user_data['email'], user_data['password']):
            user = User.where('email', user_data['email']).first()
            user.generate_token()
            return {'user': user.serialize()}
