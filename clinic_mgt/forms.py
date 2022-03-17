from genericpath import exists
from django import forms
from .models import Clinic, Doctor
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
    #cliniclocationmodel
    address = forms.CharField(max_length=100, required=False)
    # clinicmodel
    name = forms.CharField(max_length=50)


    def clean_email(self):
        email = self.cleaned_data['email']
        if Clinic.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use')
        return email

    def clean_name(self):
        name = self.cleaned_data['name']
        if Clinic.objects.filter(name=name).exists():
            raise forms.ValidationError('Name already in use')
        return name

class DoctorRegistrationForm(forms.Form):
    #usermodel
    first_name = forms.CharField(required=True, max_length=20, error_messages=error_messages)
    last_name = forms.CharField(required=True, max_length=20, error_messages=error_messages)
    email = forms.EmailField(required=True, error_messages=error_messages)

    #doctormodel


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() and Doctor.objects.filter(email=email):
            raise forms.ValidationError('Email already in use')
        return email

