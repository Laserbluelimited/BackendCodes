from genericpath import exists
from django import forms
from .models import ICOrders
from client_mgt.models import InternetClient
from clinic_mgt.models import Clinic
from prod_mgt.models import Product



class AppointmentForm(forms.Form):
    doctor = forms.ChoiceField(required=True)
    clinic = forms.ChoiceField(required=True)
    client = forms.ChoiceField(required=True)
    notes = forms.CharField(required=True)
    start_time = forms.DateTimeField(required=True)
    end_time = forms.DateTimeField(required=True)

class OrderForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=InternetClient.objects.all())
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all())
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    notes = forms.Textarea()
    date = forms.DateField(required=True)
    time_slot = forms.CharField(required=True)


    class Meta:
        model = ICOrders
        exclude = ['id', 'order_number', 'appointment', 'fulfilled', 'total_price', 'product']


class CartForm(forms.Form):
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all())
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    notes = forms.Textarea()
    date = forms.DateField(required=True)
    time_slot = forms.CharField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)



    class Meta:
        model = ICOrders
        exclude = ['id', 'order_number', 'appointment', 'fulfilled', 'total_price', 'product']
