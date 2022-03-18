from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Create your views here.
class HomePageView(View):
    def get(self, request):
        return render(request, 'display/index.html')


class AboutPageView(View):
    def get(self, request):
        return render(request, 'display/about.html')

class LocationPageView(View):
    def get(self, request):
        return render(request, 'display/location.html')

class MedicalPageView(View):
    def get(self, request):
        return render(request, 'display/medical.html')


class CBookingView(View):
    def get(self, request):
        return render(request, 'display/booking.html')


class CCouponView(View):
    def get(self, request):
        return render(request, 'display/coupon.html')


class CServiceView(View):
    def get(self, request):
        return render(request, 'display/service.html')


class CUserView(View):
    def get(self, request):
        return render(request, 'display/user.html')


class hhhhView(View):
    def get(self, request):
        return render(request, 'display/hhhh.html')
