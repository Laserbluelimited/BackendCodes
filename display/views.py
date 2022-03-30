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

class HgvPageView(View):
    def get(self, request):
        return render(request, 'display/hgvmedical.html')

class PvcPageView(View):
    def get(self, request):
        return render(request, 'display/pvcmedical.html')

class TaxiPageView(View):
    def get(self, request):
        return render(request, 'display/taxi.html')


class OtherServicesPageView(View):
    def get(self, request):
        return render(request, 'display/otherServices.html')

class BusinessClientsPageView(View):
    def get(self, request):
        return render(request, 'display/business.html')

class ICBookingView(View):
    def get(self, request):
        return render(request, 'display/booking.html')


