from dataclasses import fields
from django import forms
from .models import E_mail


class EmailForm(forms.ModelForm):
    class Meta:
        model = E_mail
        fields = ['title', 'subject', 'body_html', 'description']

        