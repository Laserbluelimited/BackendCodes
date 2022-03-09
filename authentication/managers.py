from lib2to3.pytree import Base
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Manager
import random
from skote.settings import DEFAULT_PASSWORD

class UserManager(BaseUserManager):
    def create_user(self, email, password=DEFAULT_PASSWORD, **kwargs):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and save a SuperUser with the given email and password.
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **kwargs)



class GenerateUsername():

    def __init__(self, seed, first_name):
        self.seed = seed
        self.first_name= first_name
        random.seed(self.seed)

    def generate_number(self):
        self.number = random.randint(1111,9999)
        return self.number
    
    def generate_username(self):
        self.username = f'{self.first_name}{self.generate_number()}'
        return self.username
