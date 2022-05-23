from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.views import View
from .models import Discount, Coupon, CouponUser
from .forms import CreateCouponForm
from .helpers import create_ruleset_obj
# Create your views here.


class CreateCouponView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='change_coupon'
    form_class=CreateCouponForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, 'coupon/create-coupon.html', context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            dis_val = form.cleaned_data['discount_per']
            coup_code = form.cleaned_data['code']
            
            #create discount object
            discount = Discount.objects.create(value=dis_val)

            #create ruleset object
            coupon_ruleset = create_ruleset_obj(form)

            #create coupon object
            coupon = Coupon.objects.create(code=coup_code, discount=discount, ruleset=coupon_ruleset)

            return redirect('portal:coupon-list')
        return render(request, 'coupon/create-coupon.html', context={'form':form})


class CouponTableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='view_coupon'

    def get(self, request):
        coupon = Coupon.objects.all().order_by('-id')
        paginator = Paginator(coupon, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'coupon/coupon-list.html', context={'page_obj':page_obj})

class CouponUserTableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='view_coupon'

    def get(self, request): 
        coupon_user = CouponUser.objects.all()
        paginator = Paginator(coupon_user, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'coupon/coupon-list.html', context={'page_obj':page_obj})
