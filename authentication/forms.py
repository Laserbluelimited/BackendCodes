from dataclasses import fields
import imp
from django.db import models
from django import forms
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=12)
    password = forms.CharField(required=True, max_length=50)

class ClinicRegistrationForm(forms.Form):
    #usermodel
    username = forms.CharField(required=True, max_length=12)
    password = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(required=True, max_length=30)
    #contactmodel
    address_line1 = forms.CharField(max_length=50)
    address_line2 = forms.CharField(max_length=50)
    street = forms.CharField(max_length=20)
    postal_code = forms.CharField(max_length=10)
    #clinicmodel
    name = forms.CharField(max_length=50)
