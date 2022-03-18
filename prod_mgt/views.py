from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddProductForm
from .models import Product

# Create your views here.
def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id


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
        for i in form.errors:
            print(i)
        if form.is_valid():
            product_obj = form.save(commit=False)
            product_obj.id = id_increment(Product, 1110000)

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

