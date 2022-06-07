from django.forms import modelformset_factory,BaseFormSet, formset_factory
from client_mgt.models import InternetClient
from clinic_mgt.models import Clinic
from prod_mgt.models import Product
from django import forms
from authentication.models import User

AddDriverFormSet = modelformset_factory(InternetClient, fields=('first_name', 'last_name', 'email', 'phone'), extra=1)


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=50)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('This user does not exist')
        return email


class LocationForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Clinic.objects.all())

class AppointmentForm(forms.Form):
    driver = forms.CharField(required=True, widget=forms.Select)
    product = forms.ModelChoiceField(queryset=Product.objects.all(),error_messages={'invalid_choice':'Not a valid choice'})
    date = forms.DateField(required=True )
    time_slot = forms.CharField(required=True)

class BaseBookingFormSet(BaseFormSet):
    def clean(self):
        d_and_t = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time_slot')
            d_n_t = (date, time)
            print(d_n_t)
            if d_n_t in d_and_t:
                raise forms.ValidationError("You can't pick the same time slot from the same day")
            d_and_t.append(d_n_t)


