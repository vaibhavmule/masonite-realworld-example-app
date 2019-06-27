import jwt
import pendulum

from masonite.auth import Auth
from masonite.request import Request
from masonite.helpers import password as bcrypt_password
from masonite.validation import required

from config.application import KEY
from app.User import User


class UserController:

    def __init__(self, request: Request):
        self.request = request
        self.user = request.user()

    def create(self):
        errors = self.request.validate(
            required(['user.email', 'user.password', 'user.username']),
        )

        if errors:
            self.request.status(422)
            return {'errors': errors}

        user = User.create(
            email=self.request.input('user.email'),
            password=bcrypt_password(self.request.input('user.password')),
            username=self.request.input('user.username'),
            bio=None,
            image=None,
            token=None
        )

        self.request.status(201)
        return {'user': user.serialize()}

    def current_user(self, request: Request):
        token = jwt.decode(request.header('HTTP_AUTHORIZATION').replace(
            'Token ', ''), KEY, algorithms=['HS256'])
        if pendulum.parse(token['expires']).is_past():
            request.status(401)
            return {'error': 'Your token has expired'}
        return {'user': request.user().serialize()}

    def update(self):
        self.user.update(self.request.input('user'))
        return {'user': self.user.serialize()}
