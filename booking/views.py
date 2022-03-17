from cmath import e
from email import message
import email
from multiprocessing import context
from pydoc import doc
from time import time
from urllib import response
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from authentication.models import User
from clinic_mgt.models import Clinic, Doctor
from schedules.models import ScheduleDates, TimeSlot
from client_mgt.models import InternetClient
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AppointmentForm
from .models import Appointment
import datetime

# Create your views here.
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
    template_name ='appointment/appointment-table.html' 
    def get(self, request):
        appntments = Appointment.objects.all()

        return render(request, self.template_name, context={'appointments':appntments})
 
class AppointmentRegistrationView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='appointment/appointment-form.html'
    form_class = AppointmentForm
    def get(self, request):
        form = self.form_class()
        clinics = Clinic.objects.all()
        doctors = Doctor.objects.all()
        clients = InternetClient.objects.all()

        CHOICES = []
        CHOICES2 = []
        CHOICES3 = []
        for i in doctors:
            doctor_obj = (i.user.first_name, i)
            CHOICES.append(doctor_obj)
        print(CHOICES)
        for p in clinics:
            clinic_obj = (p.name, p.name)
            CHOICES2.append(clinic_obj)
        for i in clients:
            client_obj = (i.user.email, i)
            CHOICES3.append(client_obj)
        

        form.fields['doctor'].choices = CHOICES
        form.fields['clinic'].choices = CHOICES2
        form.fields['client'].choices = CHOICES3


        return render(request, self.template_name, context={'form':form})
        
    def post(self, request):
        form = self.form_class(request.POST)

        clinics = Clinic.objects.all()
        doctors = Doctor.objects.all()
        clients = InternetClient.objects.all()

        CHOICES = []
        CHOICES2 = []
        CHOICES3 = []
        for i in doctors:
            doctor_obj = (i.email, i)
            CHOICES.append(doctor_obj)
        for p in clinics:
            clinic_obj = (p.name, p.name)
            CHOICES2.append(clinic_obj)
        for i in clients:
            client_obj = (i.email, i)
            CHOICES3.append(client_obj)
        

        form.fields['doctor'].choices = CHOICES
        form.fields['clinic'].choices = CHOICES2
        form.fields['client'].choices = CHOICES3


        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            doctor_email = form.cleaned_data['doctor']
            clinic_name = form.cleaned_data['clinic']
            client_obj = form.cleaned_data['client']
            notes = form.cleaned_data['notes']


            doctor = Doctor.objects.get(email=doctor_email)
            clinic = Clinic.objects.get(name=clinic_name)
            client = InternetClient.objects.get(email=client_obj)

            app_obj = Appointment(doctor=doctor, client=client, clinic=clinic, notes=notes, start_time=start_time, end_time=end_time)

            app_obj.save()
            return redirect('portal:app-tab')
        return render(request, self.template_name, context={'form':form})

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
    # print(response_data['dates'])
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
    print(response_data['times'])
    return JsonResponse(response_data)


