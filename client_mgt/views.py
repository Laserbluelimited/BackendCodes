from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import InternetClient, CorporateClient
from .forms import CorporateClientRegistrationForm, InternetClientRegistrationForm
from clinic_mgt.managers import AddressRequest
from authentication.models import User
from skote.settings import DEFAULT_PASSWORD
from django.contrib.auth.models import Group
from e_mail import send
from e_mail.models import E_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from authentication.helpers import account_activation_token

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

#<===============================================INDIVIDUAL CLIENTS=======================================================================>


#to display list of internet clients
class InternetClientTableView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='view_internetclient'
    
    def get(self, request):
        clients = InternetClient.objects.all().order_by('-id')
        paginator = Paginator(clients, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'client/internet-client-list.html', context={'clients':clients, 'page_obj':page_obj})



#to register internet clients in the admin portal
class InternetClientRegistrationView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='change_internetclient'
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
            address = form.cleaned_data['address']

            address_class = AddressRequest()
            geodata = address_class.get_geodata(address)

            user_obj = User.objects.create_user(email=email,is_activated=True, password=DEFAULT_PASSWORD)

            client_obj = form.save(commit=False)
            client_obj.id = id_increment(InternetClient, 1120000)
            client_obj.user = user_obj
            client_obj.address = address
            if geodata is not None:
                client_obj.long = geodata['longitude']
                client_obj.postal_code = geodata['postal_code']
                client_obj.lat = geodata['latitude']
                client_obj.city = geodata['city']
                client_obj.country = geodata['country']
 
            user_obj.save()
            client_obj.save()
            return redirect('portal:intrnt-cli-list')
        return render(request, 'client/internet-client-reg.html', context={'clients':clients, 'form':form})



#to display internet client specific details
class InternetDetailView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='view_internetclient'
    template_name ='client/internet-detail.html'
    def get(self, request, slug):
        individual = get_object_or_404(individual, slug=slug)
        return render(request, self.template_name, context={'client':individual})


class InternetClientEdit(LoginRequiredMixin,PermissionRequiredMixin,View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='change_internetclient'
    form_class = InternetClientRegistrationForm

    def get(self, request, slug):
        client=get_object_or_404(InternetClient, slug=slug)
        form = self.form_class()
        return render(request, 'client/internet-client-edit.html', context={'client':client, 'form':form})

    def post(self, request, slug):
        client=get_object_or_404(InternetClient, slug=slug)
        form = self.form_class(request.POST,instance=client)

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

            user_obj = User.objects.get(id=client.user.id)

            user_obj.email=email
            user_obj.set_password(password1)
            user_obj.save()



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
 
            client_obj.save()
            return redirect('portal:intrnt-cli-det', slug=client_obj.slug)
        return render(request, 'client/internet-client-edit.html', context={'client':client, 'form':form})


#to delete individual client

def del_ic(request, slug):
    client = get_object_or_404(InternetClient, slug=slug)
    try:

        client.delete()
        response_data = {
            'reply':'success'
        }
 
    except:

        response_data = {
            'reply':'failed'
        }
    return JsonResponse(response_data)


#<=====================================================CORPORATE CLIENT WEB AND PORTAL VIEWS, DOES NO INCLUDE CORPORATE PORTAL===================>

#to display list of corporate clients
class CorporateClientTableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='view_corporateclient'
    form_class = CorporateClientRegistrationForm

    def get(self, request):
        clients = CorporateClient.objects.all()
        paginator = Paginator(clients, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'client/cor-client-list.html', context={'clients':clients, 'page_obj':page_obj})

#to register corporate client in the admin portal
class CorporateClientRegistrationView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='change_corporateclient'
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

            user_obj = User.objects.create_user(email=email,is_activated=True, password=DEFAULT_PASSWORD)

            company_obj = form.save(commit=False)
            company_obj.user = user_obj
            company_obj.id = id_increment(CorporateClient, 1140000)
            company_obj.address = address
            if geodata is not None:
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
class CorporateDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='view_corporteclient'
    template_name ='client/crprt-detail.html'
    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        return render(request, self.template_name, context={'client':company})


#to edit corporate client information on the portal
class CorporateClientEditView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required='change_corporateclient'
    form_class = CorporateClientRegistrationForm

    def get(self, request, slug):
        client=get_object_or_404(CorporateClient, slug=slug)
        form = self.form_class()
        return render(request, 'client/cor-client-edit.html', context={'client':client, 'form':form})

    def post(self, request, slug):
        client=get_object_or_404(CorporateClient, slug=slug)
        form = self.form_class(request.POST, instance=client)
        group = Group.objects.get(name='Corporate group')
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

            user_obj = User.objects.get(id=client.user.id)
            user_obj.email =email
            user_obj.save()

            company_obj = form.save(commit=False)
            company_obj.user = user_obj
            company_obj.address = address
            company_obj.long = geodata['longitude']
            company_obj.lat = geodata['latitude']
            company_obj.city = geodata['city']
            company_obj.postal_code = geodata['postal_code']
            company_obj.country=geodata['country']
            company_obj.sub_newsletter = form.cleaned_data['sub_newsletter']
            company_obj.pur_system = form.cleaned_data['pur_system']

            company_obj.save()
            return redirect('portal:crprt-cli-det', slug=client.slug )
        return render(request, 'client/cor-client-edit.html', context={'client':client, 'form':form})

def del_cc(request, slug):
    client = get_object_or_404(CorporateClient, slug=slug)
    try:

        client.delete()
        response_data = {
            'reply':'success'
        } 
 
    except:

        response_data = {
            'reply':'failed'
        }
    return JsonResponse(response_data)



#web views

#to register corporate client on the web
class CorporateClientRegistrationWebView(View):
    form_class = CorporateClientRegistrationForm

    def get(self, request):
        form = self.form_class()
        clients = CorporateClient.objects.all()
        return render(request, 'display/application.html', context={'clients':clients, 'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        group = Group.objects.get(name='Corporate group')
        clients = CorporateClient.objects.all()
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
            if geodata is not None:
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

            #send email
            send_mail = send.SendgridClient(recipients=[user_obj.email])
            send_mail.set_template_id('d-7607031fbd0c4ea683ab1647a78b6a36')
            activation_link = get_current_site(request).domain+'/auth/cor/activate/{uidb64}/{token}'.format( uidb64=urlsafe_base64_encode(force_bytes(user_obj.pk)),
             token=account_activation_token.make_token(user_obj))
            
            print(activation_link)

            send_mail.set_template_data({'company_name':company_obj.company_name, 'activation_link':activation_link})
            send_mail.send()
            status = 'confirmation'
            return redirect('display:message', slug=company_obj.slug)
        return render(request, 'display/application.html', context={'clients':clients, 'form':form})

#To confirm web application for corporate clients

class FulfilCorporateRegistration(View):
    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        if company.user.is_activated:
            status = 'activated'
        else:
            status = 'not_activated'
        return render(request, 'display/message.html', context={'company':company, 'status':status})


class ResendCorporateConfirmation(View):
    def get(self, request, slug,):
        company = get_object_or_404(CorporateClient, slug=slug)
        if not company.user.is_activated:
            send_mail = send.SendgridClient(recipients=[company.user.email])
            send_mail.set_template_id('d-7607031fbd0c4ea683ab1647a78b6a36')
            activation_link = get_current_site(request).domain+'/auth/cor/activate/{uidb64}/{token}'.format( uidb64=urlsafe_base64_encode(force_bytes(company.user.pk)),
             token=account_activation_token.make_token(company.user))
            print(activation_link)
            send_mail.set_template_data({'company_name':company.company_name, 'activation_link':activation_link})
            send_mail.send()
            messages.add_message(request, messages.SUCCESS, 'An activation mail has been sent to you')
            return redirect('corporate_portal:login')
        else:
            return redirect('display:message', slug=company.slug)
