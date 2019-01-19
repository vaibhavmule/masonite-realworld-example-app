""" A AuthController Module """
import jwt
import pendulum

from masonite.auth import Auth
from masonite.request import Request

from api.authentication import JWTAuthentication
from api.exceptions import NoApiTokenFound, ExpiredToken, InvalidToken

from config.application import KEY 
from app.User import User


class AuthController(JWTAuthentication):
    """AuthController
    """

    def login(self, request: Request):
        user_data = request.input('user')
        if not user_data['email'] or not user_data['password']:
            return {'error': 'missing username or password'}

        if Auth(request).once().login(
            user_data['email'],
            user_data['password'],
        ):
            payload = {
                'issued': str(pendulum.now()),
                'expires': str(pendulum.now().add(minutes=1)),
                'refresh': str(pendulum.now().add(days=1)),
                'scopes': request.input('scopes'),
            }

            user = User.where('email', user_data['email']).first()
            user.token = bytes(jwt.encode(payload, KEY, algorithm='HS256')).decode('utf-8')
            user.save()
            return {'user': user.serialize() }

        return {'error': 'invalid authentication credentials'}

    def currunt_user(self, request: Request):
        token = jwt.decode(request.header('HTTP_AUTHORIZATION').replace('Token ', ''), KEY, algorithms=['HS256'])
        if pendulum.parse(token['expires']).is_past():
            raise ExpiredToken
        return {'user': request.user().serialize()}

    def update(self, request: Request):
        request.user().update(request.input('user'))
        return {'user': request.user().serialize()}