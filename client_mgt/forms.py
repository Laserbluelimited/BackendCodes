from django import forms
from authentication.models import User
from client_mgt.models import COMPANY_TYPE_CHOICES, GENDER_CHOICES, TITLE_CHOICES, CorporateClient, InternetClient
from clinic_mgt.managers import AddressRequest


geo_data = AddressRequest()


class InternetClientRegistrationForm(forms.ModelForm):
    #usermodel
    email = forms.EmailField(required=True)
    address = forms.CharField(required=False)
    dob = forms.DateField(required=False)

    class Meta:
        model = InternetClient
        fields = ['title', 'phone', 'dob', 'gender', 'first_name', 'last_name']


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        return email
    def clean_address(self):
        address = self.cleaned_data['address']
        if address:
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
    postal_code = forms.CharField(required=False)
    city = forms.CharField(required=False)
    #clientmodel
    class Meta:
        model = CorporateClient
        exclude = ['id', 'user', 'slug','address', 'long', 'lat', 'country', 'sub_newsletter', 'pur_system', ]


    def clean_email(self):
        email = self.cleaned_data['main_contact_email']
        if User.objects.filter(email=email).exists() or CorporateClient.objects.filter(main_contact_email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
        


