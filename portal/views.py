from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from clinic_mgt.models import Clinic

# Create your views here.
class AdminDashboardPageView(LoginRequiredMixin,PermissionRequiredMixin, View):
    permission_required = ('clinic_mgt.can_verify_doctors')
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        clinics = Clinic.objects.all()
        return render(request, 'dashboard-actual/dashboard.html', context={
            'clinics':clinics
        })


class TestingView(View):
    def get(self, request):
        return render(request, 'clinic/testing.html')
# class ClinicDashboardPageView(LoginRequiredMixin,PermissionRequiredMixin, View):
#     permission_required = ('clinic_mgt.can_verify_doctors')
#     login_url = '/auth/login'
#     redirect_field_name = 'redirect_to'
#     def get(self, request):
#         return render(request, 'dashboard/dashboard-blog.html')

# class DashboardPageView(LoginRequiredMixin, View):
#     permission_required = ('clinic_mgt.can_verify_doctors')
#     login_url = '/auth/login'
#     redirect_field_name = 'redirect_to'
#     def get(self, request):
#         return render(request, 'dashboard/dashboard-blog.html')
