from genericpath import exists
from django.db import models
from django import forms
from .models import Clinic
from authentication.models import User

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
    email = forms.EmailField(required=True)
    #cliniclocationmodel
    address = forms.CharField(max_length=100, required=False)
    postal_code = forms.CharField(max_length=10, required=True)
    # clinicmodel
    name = forms.CharField(max_length=50)


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use')
        return email

class DoctorRegistrationForm(forms.Form):
    #usermodel
    first_name = forms.CharField(required=True, max_length=20, error_messages=error_messages)
    last_name = forms.CharField(required=True, max_length=20, error_messages=error_messages)
    email = forms.EmailField(required=True, error_messages=error_messages)

    #doctormodel
    clinic = forms.ChoiceField(choices=CHOICES, required=True, error_messages=error_messages)


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use')
        return email

