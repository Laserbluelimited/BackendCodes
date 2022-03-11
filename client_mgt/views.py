from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InternetClient, CorporateClient
from .forms import CorporateClientRegistrationForm
from clinic_mgt.managers import AddressRequest
from authentication.models import User
# Create your views here.


class InternetClientTableView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        clients = InternetClient.objects.all()
        return render(request, 'client/internet-client-list.html', context={'clients':clients})

class CorporateClientTableView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    form_class = CorporateClientRegistrationForm

    def get(self, request):
        clients = CorporateClient.objects.all()
        return render(request, 'client/cor-client-list.html', context={'clients':clients})


class InternetClientRegistrationView(View):
    pass

class CorporateClientRegistrationView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    form_class = CorporateClientRegistrationForm

    def get(self, request):
        form = self.form_class()
        clients = CorporateClient.objects.all()
        return render(request, 'client/cor-client-reg.html', context={'clients':clients, 'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        clients = CorporateClient.objects.all()
        print('post')
        for e in form.errors:
            print(e)

        if form.is_valid():
            print('valid')
            email = form.cleaned_data['main_contact_email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            address = form.cleaned_data['address']
            username = form.cleaned_data['username']


            address_class = AddressRequest()
            geodata = address_class.get_geodata(address)
            user_obj = User.objects.create_user(email=email, password=password1, username=username)
            company_obj = form.save(commit=False)
            company_obj.user = user_obj
            company_obj.address = address
            company_obj.long = geodata['longitude']
            company_obj.lat = geodata['latitude']
            company_obj.city = geodata['city']

            user_obj.save()
            company_obj.save()
            return redirect('portal:crprt-cli-list')
        return render(request, 'client/cor-client-reg.html', context={'clients':clients, 'form':form})
