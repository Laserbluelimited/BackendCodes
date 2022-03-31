from enum import unique
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager, GenerateUsername





#  Create your models here.
class User(AbstractUser):
    username = models.CharField('username', null=True, max_length=255)
    email = models.EmailField("email_address", unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email




class Phone(models.Model):
    id = models.IntegerField('phone_id', unique=True, primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    phone_number = models.CharField('phone_number', max_length=15)
    status_id = models.IntegerField('status_id', null=True)

    def __str__(self):
        return self.phone_number

