from distutils.log import Log
from webbrowser import get
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django import forms
from authentication.models import User
from .models import Clinic, Doctor
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ClinicRegistrationForm, DoctorRegistrationForm, ClinicEditForm, DoctorEditForm
from .managers import AddressRequest
from skote.settings import DEFAULT_PASSWORD


def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id


# Create your views here.
class ClinicListView(LoginRequiredMixin,PermissionRequiredMixin,View, ):
    permission_required = ('clinic_mgt.view_clinic')
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        clinic_list = Clinic.objects.all().order_by('-id')
        paginator = Paginator(clinic_list, 5) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'clinic/clinic-list.html',context={'page_obj':page_obj} )

class DoctorListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('clinic_mgt.view_doctor')
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        doctors = Doctor.objects.all().order_by('-id')
        paginator = Paginator(doctors, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'clinic/doctor-list.html', context={'page_obj':page_obj})



class ClinicRegistration(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('clinic_mgt.change_clinic')
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='clinic/clinic-reg.html'
    form_class = ClinicRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render (request,self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']


            address_class = AddressRequest()
            geodata = address_class.get_geodata(address)


            clinic_obj = Clinic.objects.create(id=id_increment(Clinic, 1130000), name =name, address=address,postal_code=geodata['postal_code'],  long=geodata['longitude'], lat=geodata['latitude'], city=geodata['city'])
            clinic_obj.save()

            return redirect('portal:clinic-list')
            
        return render(request, self.template_name, context={'form':form})



class DoctorRegistration(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('clinic_mgt.change_doctor')
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='clinic/doctor-reg.html'
    form_class = DoctorRegistrationForm

    def get(self, request):
        form = self.form_class()
        
        return render (request,self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)


        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            doctor_user = User.objects.create_user(email=email, password=DEFAULT_PASSWORD)
            doctor_obj = Doctor.objects.create(id=id_increment(Doctor, 1170000), user=doctor_user, first_name=first_name, last_name=last_name)
            
            
            doctor_user.save()
            doctor_obj.save()

            return redirect('portal:doctor-list')
            
        return render(request, self.template_name, context={'form':form})




class DoctorDetailView(LoginRequiredMixin,PermissionRequiredMixin, View):
    permission_required = ('clinic_mgt.view_doctor')
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='clinic/doctor-detail.html'
    def get(self, request,slug):
        doctor = get_object_or_404(Doctor, slug=slug)
        return render(request, self.template_name, context={'doctor':doctor})


class ClinicDetailView(LoginRequiredMixin,PermissionRequiredMixin, View):
    permission_required = ('clinic_mgt.view_clinic')
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='clinic/clinic-detail.html'
    def get(self, request,slug):
        clinic = get_object_or_404(Clinic, slug=slug)
        return render(request, self.template_name, context={'clinic':clinic})

class ClinicEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('clinic_mgt.view_clinic')
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='clinic/clinic-edit.html'
    form_class = ClinicEditForm
    def get(self, request,slug):
        form = self.form_class()
        clinic = get_object_or_404(Clinic, slug=slug)
        return render(request, self.template_name, context={'clinic':clinic, 'form':form})
    def post(self, request, slug):
        clinic = get_object_or_404(Clinic, slug=slug)
        form = self.form_class(request.POST, instance=clinic)
        if form.is_valid():
            address = form.cleaned_data['address']
            clinic_obj = form.save(commit=False)
            address_class = AddressRequest()
            geodata = address_class.get_geodata(address)
            clinic_obj.address=address
            if geodata is not None:
                clinic_obj.postal_code=geodata['postal_code']
                clinic_obj.long=geodata['longitude']
                clinic_obj.lat=geodata['latitude']
                clinic_obj.city=geodata['city']
            clinic_obj.save()

            return redirect('portal:clinic-detail', slug=clinic_obj.slug)
            
        return render(request, self.template_name, context={'form':form, 'clinic':clinic})


class DoctorEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('clinic_mgt.change_doctor')
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='clinic/doctor-edit.html'
    form_class = DoctorEditForm

    def get(self, request, slug):
        doc = get_object_or_404(Doctor, slug=slug)
        form = self.form_class()
        
        return render (request,self.template_name, context={'form':form, 'doc':doc})

    def post(self, request, slug):
        doc = get_object_or_404(Doctor, slug=slug)
        doctor_user = User.objects.get(email=doc.user.email)
        form = self.form_class(request.POST, instance=doctor_user)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            doc_form = form.save(commit=True)

            doc.first_name = first_name
            doc.last_name = last_name
            doc.save()
            
            return redirect('portal:doctor-detail', slug=slug)
            
        return render(request, self.template_name, context={'form':form, 'doc':doc})

def del_clinic(request, slug):
    clinic = get_object_or_404(Clinic, slug=slug)
    try:

        clinic.delete()
        response_data = {
            'reply':'success'
        }
 
    except:

        response_data = {
            'reply':'failed'
        }
    return JsonResponse(response_data)


def del_doctor(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    try:

        doctor.delete()
        response_data = {
            'reply':'success'
        }
 
    except:

        response_data = {
            'reply':'failed'
        }
    return JsonResponse(response_data)
