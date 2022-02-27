from email import message
from multiprocessing import context
from django.shortcuts import render, redirect
from django.views import View
from authentication.models import User
from .models import Clinic, ClinicLocation, Doctor
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from .forms import ClinicRegistrationForm, DoctorRegistrationForm
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
        clinics=Clinic.objects.all()
        return render(request, 'clinic/clinic-list.html', context={'clinic_list':clinics})

class DoctorListView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        doctors = Doctor.objects.all()
        return render(request, 'clinic/doctor-list.html', context={'doctor_list':doctors})



class ClinicRegistration(View):
    template_name ='clinic/clinic-reg.html'
    form_class = ClinicRegistrationForm
    login_form = LoginForm

    def get(self, request):
        form = self.form_class()
        message=''
        return render (request,self.template_name, context={'form':form, 'message':message})

    def post(self, request):
        form = self.form_class(request.POST)
        message=''
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            postal_code = form.cleaned_data['postal_code']
            locality = form.cleaned_data['locality']
            num_street = form.cleaned_data['num_street']
            post_town = form.cleaned_data['post_town']

            clinic_user = User.objects.create_user(username=username, password=password, email=email)
        
            clinic_obj = Clinic.objects.create(id=id_increment(Clinic, 1130000), user=clinic_user, name =name)
            
            clinic_location = ClinicLocation.objects.create(id=id_increment(ClinicLocation, 1160000), clinic=clinic_obj, locality=locality, number_street=num_street, post_town=post_town, postal_code=postal_code)
            
            clinic_user.save()
            clinic_obj.save()
            clinic_location.save()

            return redirect('portal:clinic-list')
            
        return render(request, self.template_name, context={'form':form, 'message':message})



class DoctorRegistration(View):
    template_name ='clinic/doctor-reg.html'
    form_class = DoctorRegistrationForm
    login_form = LoginForm

    def get(self, request):
        form = self.form_class()
        message=''
        clinics = Clinic.objects.all()
        part_clinic = Clinic.objects.get(id=1)
        return render (request,self.template_name, context={'form':form, 'message':message, 'clinics':clinics, 'pc':part_clinic})

    def post(self, request):
        form = self.form_class(request.POST)
        message=''
        clinics = Clinic.objects.all()
        for i in form.errors:
            print(i)
        part_clinic = Clinic.objects.get(id=1)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            doctor_user = User.objects.create_user( username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            doctor_obj = Doctor.objects.create(id=id_increment(Doctor, 1170000), user=doctor_user, clinic=part_clinic)
            
            
            doctor_user.save()
            doctor_obj.save()

            return redirect('portal:doctor-list')
            
        return render(request, self.template_name, context={'form':form, 'message':message, 'clinics':clinics})

