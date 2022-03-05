from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from clinic_mgt.models import Clinic
from prod_mgt.models import Product

# Create your views here.

# list of things i have to define in every view:
# 1. clinics
# 2. products


class AdminDashboardPageView(LoginRequiredMixin,PermissionRequiredMixin, View):
    permission_required = ('clinic_mgt.can_verify_doctors')
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        return render(request, 'dashboard-actual/dashboard.html')


class TestingView(View):
    def get(self, request):
        return render(request, 'clinic/testing.html')


