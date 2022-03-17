from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InternetClient, CorporateClient
from .forms import CorporateClientRegistrationForm, InternetClientRegistrationForm
from clinic_mgt.managers import AddressRequest
from authentication.models import User
# Create your views here.


def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id



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
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    form_class = InternetClientRegistrationForm

    def get(self, request):
        form = self.form_class()
        clients = InternetClient.objects.all()
        return render(request, 'client/internet-client-reg.html', context={'clients':clients, 'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        clients = InternetClient.objects.all()

        if form.is_valid():
            print('valid')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            address = form.cleaned_data['address']
            username = form.cleaned_data['username']



            address_class = AddressRequest()
            geodata = address_class.get_geodata(address)
            user_obj = User.objects.create_user(email=email, password=password1, username=username)
            client_obj = form.save(commit=False)
            client_obj.id = id_increment(InternetClient, 1120000)
            client_obj.user = user_obj
            client_obj.address = address
            client_obj.long = geodata['longitude']
            client_obj.lat = geodata['latitude']
            client_obj.city = geodata['city']
            client_obj.country = geodata['country']

            user_obj.save()
            client_obj.save()
            return redirect('portal:intrnt-cli-list')
        return render(request, 'client/internet-client-reg.html', context={'clients':clients, 'form':form})

class CorporateClientRegistrationView(LoginRequiredMixin, View):
    
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
            company_obj.id = id_increment(CorporateClient, 1140000)
            company_obj.address = address
            company_obj.long = geodata['longitude']
            company_obj.lat = geodata['latitude']
            company_obj.city = geodata['city']
            company_obj.sub_newsletter = form.cleaned_data['sub_newsletter']
            company_obj.pur_system = form.cleaned_data['pursystem']

            user_obj.save()
            company_obj.save()
            return redirect('portal:crprt-cli-list')
        return render(request, 'client/cor-client-reg.html', context={'clients':clients, 'form':form})

class CorporateDetailView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='client/crprt-detail.html'
    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        return render(request, self.template_name, context={'client':company})

class InternetDetailView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='client/internet-detail.html'
    def get(self, request, slug):
        individual = get_object_or_404(individual, slug=slug)
        return render(request, self.template_name, context={'client':individual})

