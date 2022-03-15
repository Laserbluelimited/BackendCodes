from genericpath import exists
from django import forms



class AppointmentForm(forms.Form):
    doctor = forms.ChoiceField(required=True)
    clinic = forms.ChoiceField(required=True)
    client = forms.ChoiceField(required=True)
    notes = forms.CharField(required=True)
    start_time = forms.DateTimeField(required=True)
    end_time = forms.DateTimeField(required=True)
