from dataclasses import fields
import imp
from django.db import models
from django import forms
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=50)



