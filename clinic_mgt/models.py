from operator import mod
from django.db import models
from django.utils.translation import gettext_lazy as _
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
        return 'Dr. ' + self.user.first_name + ' ' + self.user.last_name

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
    postal_code = models.CharField('postal_code', max_length=10,)
    address = models.CharField('postal_code', max_length=100,)
    long = models.DecimalField('longitude', max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField('latitude', max_digits=9, decimal_places=6, null=True)


    def __str__(self):
        return self.address

class AppointmentDates(models.Model):
    db_table = 'appointment_dates'
    id = models.IntegerField('appointment_date_id', primary_key=True, unique=True)
    start_time = models.DateTimeField('start_time')
    end_time = models.DateTimeField('end_time')
    clinic = models.OneToOneField('Clinic', on_delete=models.CASCADE, unique=False)
    doctor = models.OneToOneField('Doctor', on_delete=models.CASCADE, unique=False)
    
    def __str__(self):
        return "Appointment start time: " +self.start_time

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