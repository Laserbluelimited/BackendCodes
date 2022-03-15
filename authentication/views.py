from ast import Pass
from ctypes import addressof
from multiprocessing import context
from re import template
from django.shortcuts import render, redirect
from django.views import View
from allauth.account.views import PasswordSetView,PasswordChangeView
from django.urls import reverse_lazy
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout

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
    template_name = 'authentication-actual/auth-login.html'
    form_class = LoginForm

    def get(self , request):
        form = self.form_class()
        return render (request,self.template_name, context={'form':form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('portal:dashboard')
        return render(request, self.template_name, context={'form':form})




class AuthLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('display:home-page')

