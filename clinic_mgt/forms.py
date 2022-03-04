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
    username = forms.CharField(required=True, max_length=12)
    password = forms.CharField(required=True, max_length=10, min_length=5)
    password2 = forms.CharField(required=True, max_length=10, min_length=5)
    email = forms.EmailField(required=True)
    #cliniclocationmodel
    address = forms.CharField(max_length=100, required=False)
    postal_code = forms.CharField(max_length=10, required=True)
    # clinicmodel
    name = forms.CharField(max_length=50)

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        password1 = self.cleaned_data['password']
        if password2 != password1:
            raise forms.ValidationError('Passwords are not the same')
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already in use')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use')
        return email

class DoctorRegistrationForm(forms.Form):
    #usermodel
    username = forms.CharField(required=True, max_length=12, error_messages=error_messages)
    first_name = forms.CharField(required=True, max_length=20, error_messages=error_messages)
    last_name = forms.CharField(required=True, max_length=20, error_messages=error_messages)
    password = forms.CharField(required=True, max_length=10, min_length=5, error_messages=error_messages)
    password2 = forms.CharField(required=True, max_length=10, min_length=5)
    email = forms.EmailField(required=True, error_messages=error_messages)

    #doctormodel
    clinic = forms.ChoiceField(choices=CHOICES, required=True, error_messages=error_messages)

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        password1 = self.cleaned_data['password']
        if password2 != password1:
            raise forms.ValidationError('Passwords are not the same')
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already in use')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use')
        return email

class DoctorScheduleForm(forms.Form):
    start_time = forms.DateTimeField(required=True)
    end_time = forms.DateTimeField(required=True)
    doctor = forms.ChoiceField(required=True, )