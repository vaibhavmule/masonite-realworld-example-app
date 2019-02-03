"""A AuthController Module"""

from masonite.auth import Auth
from masonite.request import Request

from app.User import User
from app.validators.AuthValidator import AuthValidator


class AuthController:
    """AuthController."""

    def login(self, request: Request):
        validate = AuthValidator(request).login_form()
        if validate.check():
            user_data = request.input('user')
            if Auth(request).once().login(user_data['email'], user_data['password']):
                user = User.where('email', user_data['email']).first()
                user.generate_token()
                return {'user': user.serialize()}
        request.status(403)
        return {'errors': validate.errors()}
