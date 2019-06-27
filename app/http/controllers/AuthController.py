from masonite.auth import Auth
from masonite.request import Request

from app.User import User


class AuthController:

    def login(self, request: Request, auth: Auth):
        email = request.input('user.email')
        password = request.input('user.password')
        if auth.once().login(email, password):
            user = User.where('email', email).first()
            user.generate_token()
            return {'user': user.serialize()}

        return {'error': 'username or password incorrect'}
