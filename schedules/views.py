from email import message
from multiprocessing import context
from pydoc import doc
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from authentication.models import User
from clinic_mgt.models import Clinic, ClinicLocation, Doctor, AppointmentDates
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DoctorScheduleForm
from .models import ScheduleDates

# Create your views here.
class DoctorScheduleCalendarView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='schedule/calendar-actual.html'    
    def get(self, request):
        schedules = ScheduleDates.objects.all()

        return render(request, self.template_name, context={'schedules':schedules})

class DoctorScheduleTableView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='schedule/doctor-schedule-table.html' 
    def get(self, request):
        schedules = ScheduleDates.objects.all()
        return render(request, self.template_name, context={'schedules':schedules})

class DoctorSchedulesRegistrationView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='schedule/schedule-form.html'
    form_class = DoctorScheduleForm 
    def get(self, request):
        form = self.form_class()
        clinics = Clinic.objects.all()
        doctors = Doctor.objects.all()
        CHOICES = []
        CHOICES2 = []
        for i in doctors:
            doctor_obj = (i.user.first_name, i.user.first_name)
            CHOICES.append(doctor_obj)
        print(CHOICES)
        for p in clinics:
            clinic_obj = (p.name, p.name)
            CHOICES2.append(clinic_obj)

        form.fields['doctor'].choices = CHOICES
        form.fields['clinic'].choices = CHOICES2


        return render(request, self.template_name, context={'form':form})
        
    def post(self, request):
        form = self.form_class(request.POST)
        

        clinics = Clinic.objects.all()
        doctors = Doctor.objects.all()
        CHOICES = []
        CHOICES2 = []
        for i in doctors:
            doctor_obj = (i.user.first_name, i.user.first_name)
            CHOICES.append(doctor_obj)
        print(CHOICES)
        for p in clinics:
            clinic_obj = (p.name, p.name)
            CHOICES2.append(clinic_obj)

        form.fields['doctor'].choices = CHOICES
        form.fields['clinic'].choices = CHOICES2

        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            doctor_name = form.cleaned_data['doctor']
            clinic_name = form.cleaned_data['clinic']


            doctor_user = User.objects.get(first_name=doctor_name)
            doctor = Doctor.objects.get(user = doctor_user)
            clinic = Clinic.objects.get(name=clinic_name)

            date_obj = ScheduleDates(start_time=start_time, end_time=end_time,clinic=clinic,doctor=doctor)

            date_obj.save()
            return redirect('portal:doc-sche-tab')
        return render(request, self.template_name, context={'form':form})
