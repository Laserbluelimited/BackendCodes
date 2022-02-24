from ast import Pass
from ctypes import addressof
from email import message
from multiprocessing import context
from re import template
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from allauth.account.views import PasswordSetView,PasswordChangeView
from django.urls import reverse_lazy
from .forms import LoginForm, ClinicRegistrationForm
from django.contrib.auth import authenticate, login, logout
from .models import User, Contact
from clinic_mgt.models import Clinic

# Create your views here.

def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id


# Authentication
class AuthLoginView(View):
    template_name = 'authentication/auth-login.html'
    form_class = LoginForm

    def get(self , request):
        form = self.form_class()
        message=''   
        return render (request,self.template_name, context={'form':form, 'message':message})
    def post(self, request):
        print('worl')
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print('yes')
            user = authenticate(username=username, password=password)
            if user is not None:
                print('hi')
                login(request, user)
                return redirect('portal:dashboard')
        else:
            print('not valid')
        message = 'Login Failed!'
        return render(request, self.template_name, context={'form':form, 'message':message})




class AuthLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('display:home-page')

class AuthClinicRegistration(View):
    template_name ='authentication/auth-register.html'
    form_class = ClinicRegistrationForm
    login_form = LoginForm

    def get(self, request):
        form = self.form_class()
        message=''
        return render (request,self.template_name, context={'form':form, 'message':message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            address_line1 = form.cleaned_data['address_line1']
            address_line2 = form.cleaned_data['address_line2']
            street = form.cleaned_data['street']
            postal_code = form.cleaned_data['postal_code']
            print('hi')


            clinic_user = User.objects.create_user(username=username, password=password, email=email)
            clinic_user.save()
            clinic_contact = Contact.objects.create(id =id_increment(Contact, 111000), user=clinic_user, address_line1=address_line1, address_line2=address_line2, street=street, postal_code=postal_code)
            clinic_contact.save()
            clinic_obj = Clinic.objects.create(id=id_increment(Clinic, 1130000), user=clinic_user, name =name, contact=clinic_contact)
            clinic_obj.save()

            return redirect('authentication:authlogin')
            
        return render(request, self.template_name, context={'form':form, 'message':message})

class AuthRegisterView(View):
    def get(self , request):    
        return render (request,'authentication/auth-register.html')
class AuthRecoverpwView(LoginRequiredMixin,View):
    def get(self , request):    
        return render (request,'authentication/auth-recoverpw.html')
class AuthLockScreenView(LoginRequiredMixin,View):
    def get(self , request):    
        return render (request,'authentication/auth-lock-screen.html')
class AuthChangePasswordView(LoginRequiredMixin,View):
    def get(self , request):    
        return render (request,'authentication/auth-password-change.html')
class AuthConfirmMailView(LoginRequiredMixin,View):
    def get(self , request):    
        return render (request,'authentication/auth-confirm-mail.html')
class AuthEmailVerificationView(LoginRequiredMixin,View):
    def get(self , request):    
        return render (request,'authentication/auth-email-verification.html') 
class AuthTwoStepVerificationView(LoginRequiredMixin,View):
    def get(self , request):    
        return render (request,'authentication/auth-two-step-verification.html')  
class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('dashboard')
class MyPasswordSetView(LoginRequiredMixin, PasswordSetView):
    success_url = reverse_lazy('dashboard')

# Main 
class DoctorRegistrationView(View):
    """
        This view is for doctor registration
        1. Doctor registers
        2. Email verification is sent to them then they verify their email
        3. Their account is added to clinic pending list awaiting clinic's confirmation
    """
    pass
class ClinicRegistrationView(View):
    """
        This view is for clinic registration
        1. Clinic registers
        2. Email verification is sent to them then they verify their email
        3. Their account is added to the pending list awaiting admin's confirmation

    """
    pass