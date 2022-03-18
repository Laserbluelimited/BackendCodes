from django import forms
from authentication.models import User
from client_mgt.models import COMPANY_TYPE_CHOICES, GENDER_CHOICES, TITLE_CHOICES, CorporateClient, InternetClient




class InternetClientRegistrationForm(forms.ModelForm):
    #usermodel
    username = forms.CharField(max_length=20,required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    address = forms.CharField(required=True)


    class Meta:
        model = InternetClient
        fields = ['title', 'phone', 'dob', 'gender', 'postal_code', 'first_name', 'last_name']


    def clean_username(self):
        user = self.cleaned_data['username']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('username already exists')
        return user
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('username already exists')
        return email
    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        password1 = self.cleaned_data['password1']
        if password2 != password1:
            raise forms.ValidationError('Passwords must be the same')
        return password2



class CorporateClientRegistrationForm(forms.ModelForm):
    #usermodel
    main_contact_email = forms.EmailField(required=True)
    username = forms.CharField(required=True, max_length=20)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    address = forms.CharField(required=True)
    pur_system = forms.ChoiceField(required=True,choices=[(True, 'Yes'), (False, 'No')])
    sub_newsletter = forms.ChoiceField(required=True,choices=[(True, 'Yes'), (False, 'No')])
    #clientmodel
    class Meta:
        model = CorporateClient
        exclude = ['id', 'user', 'slug','address', 'city', 'long', 'lat', 'country', 'sub_newsletter', 'pur_system']


    def clean_username(self):
        user = self.cleaned_data['username']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('username already exists')
        return user
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('username already exists')
    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        password1 = self.cleaned_data['password1']
        if password2 != password1:
            raise forms.ValidationError('Passwords must be the same')
        return password2
