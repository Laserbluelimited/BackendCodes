from enum import unique
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager, GenerateUsername





#  Create your models here.
class User(AbstractUser):
    username = models.CharField('Username', unique=True, max_length=20)
    email = models.EmailField("email address", unique=True, null=True)
    first_name = models.CharField('First Name', max_length=20)
    last_name = models.CharField('Last Name', max_length=20)

    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            user_obj = GenerateUsername(self.id, self.first_name)
            self.username = user_obj.generate_username()
        return super().save(*args, **kwargs)




class Phone(models.Model):
    id = models.IntegerField('phone_id', unique=True, primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    phone_number = models.CharField('phone_number', max_length=15)
    status_id = models.IntegerField('status_id', null=True)

    def __str__(self):
        return self.phone_number

