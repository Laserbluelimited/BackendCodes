from genericpath import exists
from pickle import TRUE
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
        exclude = ['id', 'order_number', 'appointment', 'fulfilled', 'total_price', 'product', 'cart']







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

    # def __init__(self, request=None, *args, **kwargs):
    #     self.request = request
    #     super(CartForm, self).__init__(*args, **kwargs)
    
    # def clean(self):
    #     if self.request:
    #         print('yes')
    #         if not self.request.session.test_cookie_worked():
    #             raise forms.ValidationError("Cookies must be enabled.")
    #         return self.cleaned_data

class CartWebForm(forms.Form):
    clinic = forms.CharField(max_length=255)
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    notes = forms.Textarea()
    date = forms.DateField(required=True)
    time_slot = forms.CharField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15)


    def clean_clinic(self):
        clinic = self.cleaned_data['clinic']
        if Clinic.objects.filter(address=clinic).exists():
            return clinic
        else:
            raise forms.ValidationError("Invalid Clinic Location. \n Select one of the listed clinics.")
