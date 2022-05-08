from django.shortcuts import render
from django.views import View
from schedules.models import ScheduleDates, TimeSlots
import datetime
from clinic_mgt.models import Clinic
from django.http import JsonResponse
# Create your views here.
class HomePageView(View):
    def get(self, request):
        return render(request, 'display/index.html')


class AboutPageView(View):
    def get(self, request):
        return render(request, 'display/about.html')

class OmedicalsPageView(View):
    def get(self, request):
        return render(request, 'display/omedicals.html')

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


class LocationPage(View):
    def get(self, request):
        return render(request, 'display/location.html')

class FAQPage(View):
    def get(self, request):
        return render(request, 'display/faqs.html')

class ContactPage(View):
    def get(self, request):
        return render(request, 'display/contact.html')




class OtherServicesPageView(View):
    def get(self, request):
        return render(request, 'display/otherServices.html')

class BusinessClientsPageView(View):
    def get(self, request):
        return render(request, 'display/business.html')

class ICBookingView(View):
    def get(self, request):
        return render(request, 'display/booking.html')

class CorporateDashboardView(View):
    def get(self, request):
        return render(request, 'display/dashboard.html')


#ajax calls
def getDates(request):

    """
    This ajax request function basically returns dates available based on a particular location.
    """
    def gen():
        """
        This generator puts the dates in the format accepted by the bootstrap datepicker
        """
        for i in dates:
            if i>= datetime.date.today():
                m = i.strftime("%d-%m-%Y")
                yield m


    location = request.GET.get('clinic')
    print(location + 's')
    clinic = Clinic.objects.get(address=location)
    dates = ScheduleDates.objects.filter(clinic=clinic).values_list('date', flat=True).distinct()
    date_list = list(gen())
    print(date_list)
    response_data = {
        'dates':date_list
    }
    return JsonResponse(response_data)

def getTimes(request):

    """
    This ajax request function basically returns times available based on a particular location and date.
    """
    def gen():
        for i in ScheduleDates.objects.filter(date=date, clinic=clinic):
            print(f"hi, {i}")
            for p in TimeSlots.objects.filter(schedule=i, status=0):
                # if p.start_time >= datetime.datetime.now().strftime('%H:%M'):
                l = p.id
                k =p.start_time.strftime('%H:%M') + ' - ' + p.end_time.strftime('%H:%M')
                yield {"id":l, "time":k}
    
    location = request.GET.get('clinic')
    clinic = Clinic.objects.get(address=location)
    date = request.GET.get('date')
    date = str(date)
    newdate = datetime.datetime.strptime(date, "%m/%d/%Y")
    date = newdate.strftime('%Y-%m-%d')

    time_obj = list(gen())
    response_data = {
        'times':time_obj
    }
    return JsonResponse(response_data)
