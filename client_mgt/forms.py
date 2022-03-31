import imp
from django import forms
from authentication.models import User
from client_mgt.models import COMPANY_TYPE_CHOICES, GENDER_CHOICES, TITLE_CHOICES, CorporateClient, InternetClient
from clinic_mgt.managers import AddressRequest


geo_data = AddressRequest()


class InternetClientRegistrationForm(forms.ModelForm):
    #usermodel
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    address = forms.CharField(required=False)


    class Meta:
        model = InternetClient
        fields = ['title', 'phone', 'dob', 'gender', 'first_name', 'last_name']


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        return email
    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        password1 = self.cleaned_data['password1']
        if password2 != password1:
            raise forms.ValidationError('Passwords must be the same')
        return password2

    def clean_address(self):
        address = self.cleaned_data['address']
        if geo_data.get_geodata(address) is not None:
            pass
        else:
            raise forms.ValidationError("Invalid Address")
        return address




class CorporateClientRegistrationForm(forms.ModelForm):
    #usermodel
    main_contact_email = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    pur_system = forms.ChoiceField(required=True,choices=[(True, 'Yes'), (False, 'No')])
    sub_newsletter = forms.ChoiceField(required=True,choices=[(True, 'Yes'), (False, 'No')])
    #clientmodel
    class Meta:
        model = CorporateClient
        exclude = ['id', 'user', 'slug','address', 'city', 'long', 'lat', 'country', 'sub_newsletter', 'pur_system', 'postal_code']


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('username already exists')
        return email

    def clean_address(self):
        address = self.cleaned_data['address']
        if geo_data.get_geodata(address) is not None:
            pass
        else:
            raise forms.ValidationError("Invalid Address")
        return address

