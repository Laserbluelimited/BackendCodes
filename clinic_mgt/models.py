from functools import partial
from operator import mod
from django.db import models
from django.utils.translation import gettext_lazy as _
from authentication.models import User
# Create your models here.


def id_increment(model, initial):
    # model_class = eval(model)
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        return initial
    last_value_id = int(last_value.id)
    new_value_id = last_value_id + 1
    return last_value_id


def clinic_id_increment():
    # model_class = eval(model)
    last_value = Clinic.objects.all().order_by('id').last()
    if not last_value:
        return 113000
    last_value_id = int(last_value.id)
    new_value_id = last_value_id + 1
    return last_value_id

def doctor_id_increment():
    # model_class = eval(model)
    last_value = Doctor.objects.all().order_by('id').last()
    if not last_value:
        return 114000
    last_value_id = int(last_value.id)
    new_value_id = last_value_id + 1
    return last_value_id

def cliniclocation_id_increment():
    # model_class = eval(model)
    last_value = ClinicLocation.objects.all().order_by('id').last()
    if not last_value:
        return 115000
    last_value_id = int(last_value.id)
    new_value_id = last_value_id + 1
    return last_value_id




class Clinic(models.Model):
    db_table = 'clinics'
    id = models.IntegerField('clinic_id', primary_key=True, unique=True)
    name = models.CharField('clinic_name', max_length=100)
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    verified = models.BooleanField('verified', default=True)
    available_to_work = models.BooleanField('available_to_work', default=True)

    class Meta:
        permissions = [
            ('can_verify_doctors', 'Can verify Doctors'),
        ]



    def __str__(self):
        return self.name

    def verify(self):
        self.verified = True
    
    def make_available(self):
        self.available_to_work = True
    
    def unverify(self):
        self.verified = False
    
    def make_unavailable(self):
        self.available_to_work=False


class Doctor(models.Model):
    db_table = 'doctors'
    id = models.IntegerField('doctor_id', primary_key=True, unique=True)
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    clinic = models.ForeignKey('Clinic', on_delete=models.CASCADE)
    verified = models.BooleanField('verified', default=True)
    available_to_work = models.BooleanField('available_to_work', default=True)


    def __str__(self):
        return 'Dr. ' + self.user.first_name

    def verify(self):
        self.verified = True
    
    def make_available(self):
        self.available_to_work = True
    
    def unverify(self):
        self.verified = False
    
    def make_unavailable(self):
        self.available_to_work=False



class ClinicLocation(models.Model):
    db_table = 'clinic_locations'
    id = models.IntegerField('clinic_location_id', primary_key=True, unique=True)
    clinic = models.OneToOneField('Clinic', on_delete=models.CASCADE)
    postal_code = models.CharField('postal_code', max_length=10)
    number_street = models.CharField('num_street', max_length=30)
    locality = models.CharField('locality', max_length=30)
    post_town = models.CharField('post_town', max_length=30)


    def __str__(self):
        return self.locality
    



# what is want to do:
# 1. create forms
# 2. enable registration in views:
#     a. first of all save the user part
#     b. then save the clinic/doctor part
# 3. test

"""
    Note to self:
    When a clinic registers, the user name and email is added to the user table
    The other clinic information is added to Clinic table
    The Contacts: address, social media handle is added the contact table
    The phone number of clinic is added to the phone number table
    The location of clinic is added to ClinicLocation table

"""