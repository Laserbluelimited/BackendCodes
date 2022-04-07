from enum import Enum
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import GroupRequiredMixin
from .forms import AddDriverFormSet, LoginForm
from client_mgt.models import InternetClient, CorporateClient

# Create your views here.


class AuthLoginView(View):
    template_name = 'cor_temp/auth-login.html'
    form_class = LoginForm

    def get(self , request):
        form = self.form_class()
        return render (request,self.template_name, context={'form':form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.groups.filter(name='Corporate group'):
                    login(request, user)
                    company = get_object_or_404(CorporateClient, user=user)
                    return redirect('corporate_portal:dashboard', slug = company.slug)
            else:
                print(form.errors)
        return render(request, self.template_name, context={'form':form})








class DashboardView(LoginRequiredMixin, GroupRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']
    
    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        return render(request, 'cor_temp/dashboard.html', context={'company':company})

class AddDriverView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = 'cor_temp/driver-form.html'
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        formset = AddDriverFormSet(queryset=InternetClient.objects.none())
        return render(request, self.template_name, context={'company':company, 'formset':formset, 'annoying':enumerate(formset)})

    def post(self, request, slug):
        formset = AddDriverFormSet(data=self.request.POST)
        company = get_object_or_404(CorporateClient, slug=slug)
        print(formset)
        if formset.is_valid():
            instances = formset.save(commit=False)
            print(instances)
            for i in instances:
                i.cor_comp = company
                i.save()
            return redirect('corporate_portal:dashboard', slug=company.slug)
        return render(request, self.template_name, context={'company':company, 'form_set':formset, 'annoying':enumerate(formset)})
        

class BookAppointmentView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = 'cor_temp/book-app.html'
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        return render(request, self.template_name, context={'company':company})
