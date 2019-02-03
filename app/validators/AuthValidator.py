from masonite.validator import Validator

from validator import Required, Pattern, Truthy


class AuthValidator(Validator):

    def login_form(self):
        return self.validate({
            'user': [Required, {
                'email': [Required],
                'password': [Required]
            }]
        })