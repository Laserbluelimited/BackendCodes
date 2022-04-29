from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator 
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class AddProductView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/auth/login'
    permission_required = ('schedules.change_product')
    redirect_field_name = 'redirect_to'
    form_class = AddProductForm
    template_name = 'prod_mgt/add-product.html'

    def get(self, request):
        form = self.form_class()
        return render (request,self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            product_obj = form.save(commit=False)
            product_obj.id = id_increment(Product, 1110000)

            product_obj.save()

            return redirect('portal:view-product')
        return render (request,self.template_name, context={'form':form})


class ViewProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/login'
    permission_required = ('schedules.change_product')
    redirect_field_name = 'redirect_to'
    template_name = 'prod_mgt/product.html'

    def get(self, request):
        products = Product.objects.all().order_by('-id')
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render (request,self.template_name, context={'page_obj':page_obj})


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/login'
    permission_required = ('schedules.view_product')
    redirect_field_name = 'redirect_to'
    template_name = 'prod_mgt/product-detail.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render (request,self.template_name, context={'product':product})

class EditProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/login'
    permission_required = ('schedules.change_product')
    redirect_field_name = 'redirect_to'
    template_name = 'prod_mgt/product-edit.html'
    form_class = AddProductForm

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = self.form_class()
        return render (request,self.template_name, context={'product':product, 'form':form})

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form= self.form_class(request.POST, instance=product)
        if form.is_valid():
            product_obj = form.save(commit=False)

            product_obj.save()

            return redirect('portal:product-detail', slug=product.slug)
        return render (request,self.template_name, context={'product':product, 'form':form})


def del_product(request, slug):
    clinic = get_object_or_404(Product, slug=slug)
    try:

        clinic.delete()
        response_data = {
            'reply':'success'
        }
 
    except:

        response_data = {
            'reply':'failed'
        }
    return JsonResponse(response_data)
