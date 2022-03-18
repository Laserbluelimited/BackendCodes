from cmath import e
from email import message
from multiprocessing import context
from django import views
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from clinic_mgt.models import Clinic
from schedules.models import ScheduleDates, TimeSlot
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrderForm
from .models import Appointment, ICOrders
import datetime
# Create your views here.

def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id


class AppointmentCalendarView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='appointment/calendar-actual.html'    
    def get(self, request):
        appntments = Appointment.objects.all()

        return render(request, self.template_name, context={'appointments':appntments})

class AppointmentTableView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='orders/appointment-table.html' 
    def get(self, request):
        appntments = Appointment.objects.all()

        return render(request, self.template_name, context={'appointments':appntments})
 

class ICOrderTableView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='orders/order-list.html' 
    def get(self, request):
        orders = ICOrders.objects.all()

        return render(request, self.template_name, context={'orders':orders})

class PlaceOrderAdminView(LoginRequiredMixin, views.View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='orders/order-form.html'
    form_class = OrderForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            clinic = form.cleaned_data['clinic']
            client = form.cleaned_data['client']
            product = form.cleaned_data['product']
            date = form.cleaned_data['date']
            time_slot = form.cleaned_data['time_slot']

            time_obj = TimeSlot.objects.get(id=time_slot)
            start_time = (datetime.datetime.strptime(time_obj.avail_times, '%H:%M')).time()
            doctor = time_obj.schedule.doctor

            app_obj = Appointment.objects.create(id=id_increment(Appointment, 114000),  doctor=doctor, clinic=clinic, client=client, date=date, start_time=start_time)
            print(app_obj.id)
            order_obj = form.save(commit=False)
            order_obj.appointment = app_obj
            order_obj.save()

            return redirect('portal:icorder-list')
        return render(request, self.template_name, context={'form':form})    







#ajax request

def getDates(request):
    location = request.GET.get('clinic')
    clinic = Clinic.objects.get(name=location)
    def gen():
        for i in ScheduleDates.objects.filter(clinic=clinic):
            m = i.date.strftime("%#d-%#m-%Y")
            yield m
    dates = list(gen())
    response_data = {
        'dates':dates
    }
    return JsonResponse(response_data)

def getTimes(request):
    location = request.GET.get('clinic')
    location= Clinic.objects.get(name=location)
    date = request.GET.get('date')
    date = datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
    def gen():
        for i in ScheduleDates.objects.filter(date=date, clinic=location):
            time_obj = TimeSlot.objects.filter(schedule=i)
            for p in time_obj:
                l=p.id
                k =p.avail_times
                yield {"id":l, "time":k}

    time_obj = list(gen())
    response_data = {
        'times':time_obj
    }
    return JsonResponse(response_data)



