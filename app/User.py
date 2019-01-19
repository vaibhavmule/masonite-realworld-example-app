"""User Model."""

from config.database import Model


class User(Model):
    """User Model."""

    __fillable__ = ['username', 'email', 'password', 'bio', 'image', 'token']

    __auth__ = 'email'
    __guarded__ = ['id', 'password']
