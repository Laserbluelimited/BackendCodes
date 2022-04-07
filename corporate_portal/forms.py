from django.forms import modelformset_factory
from client_mgt.models import InternetClient
from django import forms

AddDriverFormSet = modelformset_factory(InternetClient, fields=('first_name', 'last_name', 'email', 'phone'), extra=1)


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=50)
