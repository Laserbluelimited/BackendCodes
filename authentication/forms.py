from dataclasses import fields
import imp
from django.db import models
from django import forms
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=50)



class PasswordChangeForm(forms.Form):
    password = forms.CharField(required=True, max_length=50)
    password_again = password = forms.CharField(required=True, max_length=50)

    def clean_password_again(self):
        old = self.cleaned_data['password']
        new = self.cleaned_data['password_again']
        if new != old:
            raise forms.ValidationError('Please enter the same password in the two fields')
        return new

