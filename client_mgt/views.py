from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InternetClient, CorporateClient
from .forms import CorporateClientRegistrationForm, InternetClientRegistrationForm
from clinic_mgt.managers import AddressRequest
from authentication.models import User
from skote.settings import DEFAULT_PASSWORD
from django.contrib.auth.models import Group

# Create your views here.

#functions
def id_increment(model, initial):
    """
    This model is to increment ids of models
    model: model
    initial: first value of record if no record
    """
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id


#to display list of internet clients
class InternetClientTableView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        clients = InternetClient.objects.all()
        return render(request, 'client/internet-client-list.html', context={'clients':clients})


#to display list of corporate clients
class CorporateClientTableView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    form_class = CorporateClientRegistrationForm

    def get(self, request):
        clients = CorporateClient.objects.all()
        return render(request, 'client/cor-client-list.html', context={'clients':clients})


#to register internet clients in the admin portal
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
            #if form is valid, do the following:
            #1. get form data
            #2. call Address object to get the city, longitude, latitude and postcode of address inputed
            #3. save the client to the authentication model, User
            #4. save client to internetclient model


            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            address = form.cleaned_data['address']

            address_class = AddressRequest()
            geodata = address_class.get_geodata(address)

            user_obj = User.objects.create_user(email=email, password=password1)

            client_obj = form.save(commit=False)
            client_obj.id = id_increment(InternetClient, 1120000)
            client_obj.user = user_obj
            if geodata is not None:
                client_obj.address = address
                client_obj.long = geodata['longitude']
                client_obj.postal_code = geodata['postal_code']
                client_obj.lat = geodata['latitude']
                client_obj.city = geodata['city']
                client_obj.country = geodata['country']

            user_obj.save()
            client_obj.save()
            return redirect('portal:intrnt-cli-list')
        return render(request, 'client/internet-client-reg.html', context={'clients':clients, 'form':form})



#to regeister corporate client in the admin portal
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
        group = Group.objects.get(name='Corporate group')
        print(form.errors)
        if form.is_valid():
            #if form is valid, do the following:
            #1. get form data
            #2. call Address object to get the city, longitude, latitude and postcode of address inputed
            #3. save the client to the authentication model, User
            #4. save client to corporateclient model
            
            email = form.cleaned_data['main_contact_email']
            address = form.cleaned_data['address']


            address_class = AddressRequest()
            geodata = address_class.get_geodata(address)

            user_obj = User.objects.create_user(email=email, password=DEFAULT_PASSWORD)

            company_obj = form.save(commit=False)
            company_obj.user = user_obj
            company_obj.id = id_increment(CorporateClient, 1140000)
            company_obj.address = address
            company_obj.long = geodata['longitude']
            company_obj.lat = geodata['latitude']
            company_obj.city = geodata['city']
            company_obj.postal_code = geodata['postal_code']
            company_obj.country=geodata['country']
            company_obj.sub_newsletter = form.cleaned_data['sub_newsletter']
            company_obj.pur_system = form.cleaned_data['pur_system']

            user_obj.save()
            group.user_set.add(user_obj)
            company_obj.save()
            return redirect('portal:crprt-cli-list')
        return render(request, 'client/cor-client-reg.html', context={'clients':clients, 'form':form})



#to display corporate client specific details
class CorporateDetailView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='client/crprt-detail.html'
    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        return render(request, self.template_name, context={'client':company})



#to display internet client specific details
class InternetDetailView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='client/internet-detail.html'
    def get(self, request, slug):
        individual = get_object_or_404(individual, slug=slug)
        return render(request, self.template_name, context={'client':individual})


#web views
class CorporateClientRegistrationWebView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    form_class = CorporateClientRegistrationForm

    def get(self, request):
        form = self.form_class()
        clients = CorporateClient.objects.all()
        return render(request, 'display/application.html', context={'clients':clients, 'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        group = Group.objects.get(name='Corporate group')
        clients = CorporateClient.objects.all()
        for i in form.errors:
            print(i)

        if form.is_valid():
            #if form is valid, do the following:
            #1. get form data
            #2. call Address object to get the city, longitude, latitude and postcode of address inputed
            #3. save the client to the authentication model, User
            #4. save client to corporateclient model
            
            email = form.cleaned_data['main_contact_email']
            address = form.cleaned_data['address']


            address_class = AddressRequest()
            geodata = address_class.get_geodata(address)

            user_obj = User.objects.create_user(email=email, password=DEFAULT_PASSWORD)

            company_obj = form.save(commit=False)
            company_obj.user = user_obj
            company_obj.id = id_increment(CorporateClient, 1140000)
            company_obj.address = address
            company_obj.long = geodata['longitude']
            company_obj.lat = geodata['latitude']
            company_obj.city = geodata['city']
            company_obj.postal_code = geodata['postal_code']
            company_obj.country=geodata['country']
            company_obj.sub_newsletter = form.cleaned_data['sub_newsletter']
            company_obj.pur_system = form.cleaned_data['pur_system']

            user_obj.save()
            company_obj.save()
            group.user_set.add(user_obj)
            return redirect('display:home-page')
        return render(request, 'display/application.html', context={'clients':clients, 'form':form})
