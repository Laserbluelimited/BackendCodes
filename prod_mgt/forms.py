from genericpath import exists
from django import forms
from .models import Product



class AddProductForm(forms.Form):
    name_of_prod = forms.CharField(required=True, max_length=30)
    price = forms.IntegerField(required=True)

    def clean_name_of_prod(self):
        name_of_prod = self.cleaned_data['name_of_prod']
        if Product.objects.filter(name_of_prod=name_of_prod).exists():
            raise forms.ValidationError("Product already exists")
        return name_of_prod