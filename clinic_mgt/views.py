from email import message
from multiprocessing import context
from pydoc import doc
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from authentication.models import User
from .models import Clinic, ClinicLocation, Doctor, AppointmentDates
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ClinicRegistrationForm, DoctorRegistrationForm, DoctorScheduleForm
from .managers import AddressRequest
from authentication.forms import LoginForm


def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id


# Create your views here.
class ClinicListView(LoginRequiredMixin,View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        return render(request, 'clinic/clinic-list.html', )

class DoctorListView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        doctors = Doctor.objects.all()
        return render(request, 'clinic/doctor-list.html', context={'doctor_list':doctors})



class ClinicRegistration(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='clinic/clinic-reg.html'
    form_class = ClinicRegistrationForm
    login_form = LoginForm

    def get(self, request):
        form = self.form_class()
        return render (request,self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            postal_code = form.cleaned_data['postal_code']


            address_class = AddressRequest()
            geodata = address_class.get_geodata(address)


            clinic_user = User.objects.create_user(username=username, password=password, email=email)
            clinic_obj = Clinic.objects.create(id=id_increment(Clinic, 1130000), user=clinic_user, name =name)
            clinic_location = ClinicLocation.objects.create(id=id_increment(ClinicLocation, 1160000), clinic=clinic_obj, address=address,postal_code=postal_code,  long=geodata['longitude'], lat=geodata['latitude'])
            
            clinic_user.save()
            clinic_obj.save()
            clinic_location.save()

            return redirect('portal:clinic-list')
            
        return render(request, self.template_name, context={'form':form})



class DoctorRegistration(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='clinic/doctor-reg.html'
    form_class = DoctorRegistrationForm
    login_form = LoginForm

    def get(self, request):
        form = self.form_class()
        clinics = Clinic.objects.all()
        CHOICES = []
        for i in clinics:
            clinic_obj = (i.name, i.name)
            CHOICES.append(clinic_obj)

        form.fields['clinic'].choices = CHOICES
        
        return render (request,self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        clinics = Clinic.objects.all()

        CHOICES = []
        for i in clinics:
            clinic_obj = (i.name, i.name)
            CHOICES.append(clinic_obj)
        form.fields['clinic'].choices = CHOICES

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            clinic = form.cleaned_data['clinic']

            clinic_sel = Clinic.objects.get(name=clinic)
            doctor_user = User.objects.create_user( username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            doctor_obj = Doctor.objects.create(id=id_increment(Doctor, 1170000), user=doctor_user, clinic=clinic_sel)
            
            
            doctor_user.save()
            doctor_obj.save()

            return redirect('portal:doctor-list')
            
        return render(request, self.template_name, context={'form':form})


class DoctorSchedules(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='calendar-actual.html'    
    def get(self, request, url_para):
        clinic = get_object_or_404(Clinic, id=url_para)
        return render(request, self.template_name, context={'url_para':url_para,'clinic':clinic})

class ViewSchedule(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='schedule/view-schedule.html' 
    def get(self, request, url_para):
        clinic = get_object_or_404(Clinic, id=url_para)
        dates = AppointmentDates.objects.filter(clinic=clinic)
        return render(request, self.template_name, context={'url_para':url_para,  'dates':dates})

class DoctorSchedulesRegistration(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='schedule/schedule-form.html'
    form_class = DoctorScheduleForm 
    def get(self, request, url_para):
        form = self.form_class()
        clinic = get_object_or_404(Clinic, id=url_para)
        CHOICES = []
        doctors = Doctor.objects.filter(clinic=clinic)
        for i in doctors:
            doctor_obj = (i.user.first_name, i.user.first_name)
            CHOICES.append(doctor_obj)
        print(CHOICES)

        form.fields['doctor'].choices = CHOICES

        clinics = Clinic.objects.all()
        doctors = Doctor.objects.filter(clinic=clinic)

        return render(request, self.template_name, context={'url_para':url_para,  'clinic':clinic, 'doctors':doctors, 'form':form})
        
    def post(self, request, url_para):
        form = self.form_class(request.POST)
        clinic = get_object_or_404(Clinic, id=url_para)
        

        CHOICES = []
        doctors = Doctor.objects.filter(clinic=clinic)
        for i in doctors:
            doctor_obj = (i.user.first_name, i.user.first_name)
            CHOICES.append(doctor_obj)
        print(CHOICES)
        form.fields['doctor'].choices = CHOICES
        
        clinics = Clinic.objects.all()

        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            doctor_name = form.cleaned_data['doctor']

            doctor_user = User.objects.get(first_name=doctor_name)
            doctor = Doctor.objects.get(user = doctor_user)

            date_obj = AppointmentDates(start_time=start_time, end_time=end_time,clinic=clinic,doctor=doctor)

            date_obj.save()
            return redirect('portal:doc-sche-tab', url_para=clinic.id)
        return render(request, self.template_name, context={'url_para':url_para, 'clinic':clinic, 'doctors':doctors, 'form':form})
