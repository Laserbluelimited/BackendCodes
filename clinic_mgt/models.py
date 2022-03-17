from operator import mod
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify

# Create your models here.






class Clinic(models.Model):
    id = models.IntegerField('clinic_id', primary_key=True, unique=True)
    name = models.CharField('clinic_name', max_length=100)
    email = models.EmailField('email', unique=True, null=True)
    postal_code = models.CharField('postal_code', max_length=10,)
    address = models.CharField('postal_code', max_length=100,)
    long = models.DecimalField('longitude', max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField('latitude', max_digits=9, decimal_places=6, null=True)
    city = models.CharField('city', max_length=100,)





    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email
    
    def get_city(self):
        return self.city

    def get_address(self):
        return self.address



class Doctor(models.Model):
    db_table = 'doctors'
    id = models.IntegerField('doctor_id', primary_key=True, unique=True)
    first_name = models.CharField('first_name', max_length=100)
    last_name = models.CharField('last_name', max_length=100)
    email = models.EmailField('email', unique=True)
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    verified = models.BooleanField('verified', default=True)
    available_to_work = models.BooleanField('available_to_work', default=True)
    slug = models.SlugField(max_length=255, help_text='Unique Value for product page URL, created from name.')


    def save(self, *args, **kwargs):
        if not self.slug:
            name = self.first_name + str(self.id)
            self.slug = slugify(name)
        return super(Doctor,self).save(*args, **kwargs)

    def __str__(self):
        return 'Dr. ' + self.first_name + ' ' + self.last_name


    def get_name(self):
        return self.first_name + ' ' + self.last_name

    def get_email(self):
        return self.email


    def verify(self):
        self.verified = True
    
    def make_available(self):
        self.available_to_work = True
    
    def unverify(self):
        self.verified = False
    
    def make_unavailable(self):
        self.available_to_work=False



