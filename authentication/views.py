from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from allauth.account.views import PasswordSetView,PasswordChangeView
from django.urls import reverse_lazy


# Create your views here.

# Authentication
class AuthLoginView(LoginRequiredMixin,View):
    def get(self , request):    
        return render (request,'authentication/auth-login.html')
class AuthRegisterView(LoginRequiredMixin,View):
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