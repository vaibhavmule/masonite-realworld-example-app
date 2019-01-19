from masonite.request import Request
from masonite.helpers import password as bcrypt_password

from api.resources import Resource
from api.serializers import JSONSerializer
from api.authentication import JWTAuthentication
from masonite.helpers import password as bcrypt_password

from app.User import User


class UserResource(Resource, JSONSerializer):
    model = User
    methods = ['create', 'index', 'show']

    def create(self):
        user_data = self.request.input('user')
        user = self.model.create(
            email=user_data['email'],
            password=bcrypt_password(user_data['password']),
            username=user_data['username'],
            bio=None,
            image=None,
            token=None
        )
        return {'user': user.serialize()}
