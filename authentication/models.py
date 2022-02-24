from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager

def contact_id_increment():
    # model_class = eval(model)
    last_value = Contact.objects.all().order_by('id').last()
    if not last_value:
        return 111000
    last_value_id = int(last_value.id)
    new_value_id = last_value_id + 1
    return last_value_id

def phone_id_increment():
    # model_class = eval(model)
    last_value = Phone.objects.all().order_by('id').last()
    if not last_value:
        return 112000
    last_value_id = int(last_value.id)
    new_value_id = last_value_id + 1
    return last_value_id




#  Create your models here.
class User(AbstractUser):
    username = models.CharField('Username', unique=True, max_length=20)
    email = models.EmailField("email address", unique=True)

    objects = UserManager()

    def __str__(self):
        return self.username

class Contact(models.Model):

    id = models.IntegerField('contact_id', unique=True, primary_key=True, default=1110000)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street = models.CharField('street', max_length=50)
    address_line1 = models.CharField('Address_Line_1', max_length=100)
    address_line2 = models.CharField('Address line 2', max_length=100)
    postal_code = models.CharField('Postal_code', max_length=10)

    def __str__(self):
        return self.user.email

class Phone(models.Model):
    id = models.IntegerField('phone_id', unique=True, primary_key=True, default=phone_id_increment)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    phone_number = models.CharField('phone_number', max_length=15)
    status_id = models.IntegerField('status_id', null=True)

    def __str__(self):
        return self.phone_number

