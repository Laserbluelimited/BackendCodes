from django import forms
from authentication.models import User
from client_mgt.models import COMPANY_TYPE_CHOICES, GENDER_CHOICES, TITLE_CHOICES, CorporateClient, InternetClient




class InternetClientRegistrationForm(forms.Form):
    #usermodel
    first_name = forms.CharField(required=True, max_length=20)
    last_name = forms.CharField(required=True, max_length=20)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    #clientmodel
    # title = forms.ChoiceField(choices=TITLE_CHOICES, required=True, )
    # phone = forms.IntegerField(required=True)
    # dob = forms.DateField()
    # gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    # address = forms.CharField(required=True)
    # postal_code = forms.CharField(required=True)
    class Meta:
        model = InternetClient
        fields = ['title', 'phone', 'dob', 'gender', 'address', 'postal_code']


    def clean_username(self):
        user = self.cleaned_data['username']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('username already exists')
        return user
    def clean_email(self):
        email = self.cleaned_data['username']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('username already exists')
        return email


class CorporateClientRegistrationForm(forms.ModelForm):
    #usermodel
    main_contact_email = forms.EmailField(required=True)
    username = forms.CharField(required=True, max_length=20)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    address = forms.CharField(required=True)

    #clientmodel
    class Meta:
        model = CorporateClient
        exclude = ['id', 'user', 'slug','addres', 'city', 'long', 'lat', 'country', 'auth_prsnl_first_name', 'auth_prsnl_last_name', 'auth_prsnl_title', ]

    


    def clean_username(self):
        user = self.cleaned_data['username']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('username already exists')
        return user
    def clean_email(self):
        email = self.cleaned_data['username']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('username already exists')
        return email
