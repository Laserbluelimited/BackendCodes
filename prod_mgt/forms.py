from genericpath import exists
from django import forms
from .models import Product



class AddProductForm(forms.ModelForm):
    descripton = forms.CharField(required=False)
    meta_keywords = forms.CharField(required=False)
    meta_description = forms.CharField(required=False)

    class Meta:
        model = Product
        exclude = ['slug', 'currency', 'image', 'is_active', 'id']

    # def clean_name_of_prod(self):
    #     name_of_prod = self.cleaned_data['name_of_prod']
    #     if Product.objects.filter(name_of_prod=name_of_prod).exists():
    #         raise forms.ValidationError("Product already exists")
    #     return name_of_prod 