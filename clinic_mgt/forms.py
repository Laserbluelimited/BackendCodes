from django.db import models
from django import forms
from .models import Clinic

CHOICES = []
clinics = Clinic.objects.all()
for i in clinics:
    clinic_obj = (i, i)
    CHOICES.append(clinic_obj)

error_messages = {
    'required':'Please fill this field',
    'invalid':'Wrong Format'
}

class ClinicRegistrationForm(forms.Form):
    #usermodel
    username = forms.CharField(required=True, max_length=12)
    password = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(required=True)
    #cliniclocationmodel
    num_street = forms.CharField(max_length=50)
    locality = forms.CharField(max_length=50)
    post_town = forms.CharField(max_length=20)
    postal_code = forms.CharField(max_length=10)
    # clinicmodel
    name = forms.CharField(max_length=50)

class DoctorRegistrationForm(forms.Form):
    #usermodel
    username = forms.CharField(required=True, max_length=12, error_messages=error_messages)
    first_name = forms.CharField(required=True, max_length=12, error_messages=error_messages)
    last_name = forms.CharField(required=True, max_length=12, error_messages=error_messages)
    password = forms.CharField(required=True, max_length=50, error_messages=error_messages)
    email = forms.EmailField(required=True, error_messages=error_messages)
    #doctormodel
    # clinic = forms.ChoiceField(choices=CHOICES, required=True, error_messages=error_messages)
