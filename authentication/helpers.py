import math
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import random

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
        )


class PasswordResetToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
        )


account_activation_token = AccountActivationTokenGenerator()
password_reset_token = PasswordResetToken()

def generate_password():
    string = "1234567890qwertyuiopasdfghjklzxcvbnm=+()QWERTYUIOPLKJHGFDSAZXCVBNM,"
    password = ''
    for i in range(6):
        password+=string[math.floor(random.random()*len(string))]
    return password
