from django.db import models
from django.utils.translation import gettext_lazy as _
from authentication.models import id_increment
# Create your models here.



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
    id = models.IntegerField('clinic_id', primary_key=True, unique=True, default=clinic_id_increment)
    name = models.CharField('clinic_name', max_length=100)
    user = models.OneToOneField('User', on_delete=models.CASCADE)


class Doctor(models.Model):
    db_table = 'doctors'
    id = models.IntegerField('doctor_id', primary_key=True, unique=True, default=doctor_id_increment)
    contact = models.OneToOneField('Contact', on_delete=models.CASCADE)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    clinic = models.ForeignKey('Clinic', on_delete=models.CASCADE)
    date_joined = models.DateField('date_joined', auto_now_add=True)



class ClinicLocation(models.Model):
    db_table = 'clinic_locations'
    id = models.IntegerField('clinic_location_id', primary_key=True, unique=True, default=cliniclocation_id_increment)
    clinic = models.OneToOneField('Clinic', on_delete=models.CASCADE)
    postal_code = models.CharField('postal_code', max_length=10)
    

