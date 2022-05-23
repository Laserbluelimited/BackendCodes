from random import choices
from django import forms
from pyparsing import empty
from authentication.models import User

TRUE_FALSE_CHOICES = ((True, 'Yes'), (False, 'No'))


class CreateCouponForm(forms.Form):
    #coupon
    discount_per = forms.IntegerField(required=True)
    code = forms.CharField(max_length=12, required=True)

    #RULESET
    #1. Allowed Users
    all_users = forms.ChoiceField(required=False, choices=TRUE_FALSE_CHOICES)
    all_cor_users = forms.ChoiceField(required=False, choices=TRUE_FALSE_CHOICES)
    all_ind_users = forms.ChoiceField(required=False, choices=TRUE_FALSE_CHOICES)
    users = forms.ModelMultipleChoiceField(required=False, queryset=User.objects.all())

    #2. Max Uses
    max_uses = forms.IntegerField(required=False)
    is_infinite = forms.ChoiceField(required=False, choices=TRUE_FALSE_CHOICES)
    uses_per_user = forms.IntegerField(required=False)

    #3. Validity rule
    expiration_date = forms.DateTimeField(required=True)
    is_active = forms.ChoiceField(required=False, choices=TRUE_FALSE_CHOICES)

    def clean_all_cor_users(self):
        all_users = self.cleaned_data.get('all_users')
        ind_users = self.cleaned_data.get('all_ind_users')
        users = self.cleaned_data.get('users')
        if self.cleaned_data.get('all_cor_users')=='True':
            if all_users=='True' or ind_users=='True':
                raise forms.ValidationError('Please select one from this section')
            elif users is not None:
                print(users)
                raise forms.ValidationError('Please select one from this section')
        return self.cleaned_data.get('all_cor_users')

    def clean_users(self):
        all_users = self.cleaned_data.get('all_users')
        cor_users = self.cleaned_data.get('all_cor_users')
        ind_users = self.cleaned_data.get('all_ind_users')
        users = self.cleaned_data.get('users')
        if users.exists():
            print(users)
            if all_users=='True' or cor_users=='True' or ind_users=='True':
                raise forms.ValidationError('Please select one from this section')
        return self.cleaned_data.get('users')

    def clean_all_users(self):
        ind_users = self.cleaned_data.get('all_ind_users')
        cor_users = self.cleaned_data.get('all_cor_users')
        
        users = self.cleaned_data.get('users')
        if self.cleaned_data.get('all_users') =='True':
            if cor_users=='True' or ind_users=='True':
                raise forms.ValidationError('Please select one from this section')
            elif users is not None:
                raise forms.ValidationError('Please select one from this section')
        return self.cleaned_data.get('all_users')
