import jwt
import pendulum

from masonite.auth import Auth
from masonite.request import Request
from masonite.helpers import password as bcrypt_password

from api.authentication import JWTAuthentication
from api.exceptions import NoApiTokenFound, ExpiredToken, InvalidToken

from config.application import KEY 
from app.User import User


class UserController:
    """UserController""" 

    def create(self, request: Request):
        user_data = request.input('user')
        user = User.create(
            email=user_data['email'],
            password=bcrypt_password(user_data['password']),
            username=user_data['username'],
            bio=None,
            image=None,
            token=None
        )
        return {'user': user.serialize()}

    def currunt_user(self, request: Request):
        token = jwt.decode(request.header('HTTP_AUTHORIZATION').replace('Token ', ''), KEY, algorithms=['HS256'])
        if pendulum.parse(token['expires']).is_past():
            raise ExpiredToken
        return {'user': request.user().serialize()}

    def update(self, request: Request):
        request.user().update(request.input('user'))
        return {'user': request.user().serialize()}
