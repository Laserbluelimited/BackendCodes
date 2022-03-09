from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddProductForm
from .models import Product

# Create your views here.
class AddProductView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    form_class = AddProductForm
    template_name = 'prod_mgt/add-product.html'

    def get(self, request):
        form = self.form_class()
        return render (request,self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            name_of_prod = form.cleaned_data['name_of_prod']
            price = form.cleaned_data['price']

            product_obj = Product.objects.create(name_of_prod=name_of_prod, price=price)
            product_obj.save()

            return redirect('portal:view-product')
        return render (request,self.template_name, context={'form':form})


class ViewProductView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name = 'prod_mgt/product.html'

    def get(self, request):
        return render (request,self.template_name)


class ProductDetailView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name = 'prod_mgt/product-detail.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render (request,self.template_name, context={'product':product})

