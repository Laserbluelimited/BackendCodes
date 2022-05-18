from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from authentication.models import User
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import GroupRequiredMixin
from .forms import AddDriverFormSet, LoginForm,BaseBookingFormSet, LocationForm, AppointmentForm
from client_mgt.models import InternetClient, CorporateClient
from clinic_mgt.managers import AddressRequest
from django.forms import formset_factory
from django import forms
from prod_mgt.models import Product
from django.http import JsonResponse, HttpResponseForbidden
import datetime
from schedules.models import ScheduleDates, TimeSlots
from booking.models import CCart, CorporateAppointment, increment_capp_no, CCInvoice, CCOrders
from . import cart
from client_mgt.forms import CorporateClientRegistrationForm, InternetClientRegistrationForm
from payment import stripe
from payment.models import Payment
from skote.settings import DEFAULT_PASSWORD



#function to book appointment
def book_appointment(model, time_slot, client,c_client,product,appointment_no, status=0,  notes=None,):

    """
    This function basically helps to book an appointment
    model: Appointment model
    schedule: time slot object/instance
    client: internet client object/instance
    status: 0 if it has not been paid for, 1 if it has been paid for

    if status is 0, it updates the schedule object to 1(temporarily unavailable)
    if status is 1, it updates the schedule object to 2(has been paid for)
    
    
    """
    app_obj = model.objects.create( time_slot=time_slot, client=client, status=status, notes=notes, c_client=c_client, product=product, appointment_no=appointment_no )
    if status == 0:
        time_slot.status = 1
        time_slot.save()
    elif status == 1:
        time_slot.status = 2
        time_slot.save()
    return app_obj

def check_user(slug_user, current_user):
    if slug_user!=current_user:
        return HttpResponseForbidden()
        






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
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']
    
    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        check_user(current_user=request.user, slug_user=company.user)
        return render(request, 'cor_temp/dashboard.html', context={'company':company})

class AddDriverView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = 'cor_temp/driver-form.html'
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        check_user(current_user=request.user, slug_user=company.user)
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
    template_name = 'cor_temp/booking.html'
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']
    company=None


    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        check_user(current_user=request.user, slug_user=company.user)
        if "cor_cart_id" in request.session:
            return redirect('corporate_portal:checkout', slug=company.slug)
        else:
            request.session.set_test_cookie()
        
        l_form = LocationForm()
        d_form = formset_factory(AppointmentForm, extra=1, formset=BaseBookingFormSet)
        d_form = d_form()
        d_query = InternetClient.objects.filter(cor_comp=company)
        return render(request, self.template_name, context={'company':company,  'l_form':l_form, 'd_form':d_form, 'annoying':enumerate(d_form), 'd_query':d_query})
        

    def post(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        l_form = LocationForm()
        d_form = formset_factory(form=AppointmentForm, extra=1, formset=BaseBookingFormSet)
        d_form = d_form(data=self.request.POST)
        
        if d_form.is_valid() and request.session.test_cookie_worked():
            quantity = 0
            price = 0
            appointment_no = increment_capp_no()
            for form in d_form:
                driver = form.cleaned_data['driver']
                driver = InternetClient.objects.get(id=int(driver))
                product = form.cleaned_data['product']
                time_slot = form.cleaned_data['time_slot']

                #3
                sche_obj = TimeSlots.objects.get(id=time_slot)
                app_obj = book_appointment(CorporateAppointment, time_slot=sche_obj, status=0, client=driver, c_client=company, product=product, appointment_no=appointment_no)
                quantity+=1
                price+=product.price

                #4
            cart.add_to_cart(request, client=company, appointment=appointment_no, quantity=quantity, price=price)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            


            
            return redirect('corporate_portal:checkout', slug = company.slug)
        else:
            print(d_form.errors)
            print(d_form.non_form_errors())

    

        return render(request, self.template_name, context={'company':company,  'l_form':l_form, 'd_form':d_form, 'annoying':enumerate(d_form)})


class CheckoutView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = 'cor_temp/checkout.html'
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        check_user(current_user=request.user, slug_user=company.user)
        if "cor_cart_id" in request.session:
            basket_id = request.session['cor_cart_id']
            basket = CCart.objects.get(cart_id=basket_id)
            appointments = CorporateAppointment.objects.filter(appointment_no =basket.appointment)

            print(basket.price)
        else:
            basket = 'empty'
            return redirect('corporate_portal:booking', slug=company.slug)

        return render(request, self.template_name, context={'company':company, 'appointments':appointments, 'basket':basket})

    def post(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        if "cor_cart_id" in request.session:
            cart_id = request.session['cor_cart_id']
            cart_obj = CCart.objects.get(cart_id=cart_id)
            return stripe.cccheckout_stripe(cart_id=cart_obj)
        else:
            return redirect('corporate_portal:booking', slug=company.slug)


class DeleteCartView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = 'cor_temp/checkout.html'
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        check_user(current_user=request.user, slug_user=company.user)
        if "cor_cart_id" in request.session:
            del request.session['cor_cart_id']
            return redirect('corporate_portal:booking', slug=company.slug)
        else:
            return redirect('corporate_portal:booking', slug=company.slug)



class DriverListView(LoginRequiredMixin, GroupRequiredMixin, View):
    permission_required = ('clinic_mgt.view_doctor')
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']
    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        check_user(current_user=request.user, slug_user=company.user)
        drivers = InternetClient.objects.filter(cor_comp=company).order_by('-id')
        paginator = Paginator(drivers, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'cor_temp/driver-table.html', context={'page_obj':page_obj, 'company':company})


class OrderListView(LoginRequiredMixin,GroupRequiredMixin, View):
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        check_user(slug_user=company.user, current_user=request.user)
        orders = CCOrders.objects.filter(c_client=company)
        return render(request, 'cor_temp/orders.html', context={'company':company, 'orders':orders})

class CompanyEditView(LoginRequiredMixin,GroupRequiredMixin, View):
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']
    form_class = CorporateClientRegistrationForm

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        check_user(slug_user=company.user, current_user=request.user)
        form = self.form_class()
        return render(request, 'cor_temp/company-edit.html', context={'company':company, 'form':form})

    def post(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        form = self.form_class(request.POST, instance=company)
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
            user_obj = User.objects.get(email=email)


            company_obj = form.save(commit=False)
            user_obj.email = email
            company_obj.main_contact_email = email
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
            return redirect('corporate_portal:dashboard', slug=company_obj.slug)
        return render(request, 'cor_temp/company-edit.html', context={'company':company, 'form':form})

class DriverEditView(LoginRequiredMixin,GroupRequiredMixin, View):
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']
    form_class = InternetClientRegistrationForm

    def get(self, request, slug, driver):
        company = get_object_or_404(CorporateClient, slug=slug)
        driver = get_object_or_404(InternetClient, slug=driver)
        form = self.form_class()
        clients = InternetClient.objects.all()
        return render(request, 'cor_temp/driver-edit.html', context={'company':company,'driver':driver, 'form':form})

    def post(self, request, slug, driver):
        company = get_object_or_404(CorporateClient, slug=slug)
        driver = get_object_or_404(InternetClient, slug=driver)
        form = self.form_class(request.POST, instance=driver)

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


            client_obj = form.save(commit=False)
            client_obj.email = email
            if address:
                client_obj.address = address
                client_obj.long = geodata['longitude']
                client_obj.postal_code = geodata['postal_code']
                client_obj.lat = geodata['latitude']
                client_obj.city = geodata['city']
                client_obj.country = geodata['country']
 
            client_obj.save()
            return redirect('corporate_portal:driver-list', slug=company.slug)
        return render(request, 'cor_temp/driver-edit.html', context={'company':company,'driver':driver, 'form':form})


class InvoiceView(LoginRequiredMixin,GroupRequiredMixin, View):
    login_url = '/business/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']

    def get(self, request, slug, order_no):
        company = get_object_or_404(CorporateClient, slug=slug)
        invoice = get_object_or_404(CCInvoice, order=order_no)
        order = CCOrders.objects.filter(order_number=invoice.order).first()
        appointments = CorporateAppointment.objects.filter(appointment_no=order.appointment)
        total = float(invoice.payment.total_amount)/100

        return render(request, 'payment/invoice_cor.html', context={'invoice':invoice,'apps':appointments,'total':total, 'order':order, 'company':company})



def getDates(request, slug):

    """
    This ajax request function basically returns dates available based on a particular location.
    """
    def gen():
        """
        This generator puts the dates in the format accepted by the bootstrap datepicker
        """
        for i in new_dates:
            if i>= datetime.date.today():
                m = i.strftime("%d-%m-%Y")
                yield m


    location = request.GET.get('clinic')
    dates = ScheduleDates.objects.filter(clinic=location)
    for i in dates:
        if TimeSlots.objects.filter(schedule=i, status=0).exists()==False:
            dates = dates.exclude(id=i.id)
    new_dates = dates.values_list('date', flat=True).distinct()
    date_list = list(gen())
    response_data = {
        'dates':date_list
    }
    print(new_dates)
    return JsonResponse(response_data)

def getTimes(request, slug):

    """
    This ajax request function basically returns times available based on a particular location and date.
    """
    def gen():
        for i in ScheduleDates.objects.filter(date=date, clinic=location):
            for p in TimeSlots.objects.filter(schedule=i, status=0):
                
                l = p.id
                k =p.start_time.strftime('%H:%M') + ' - ' + p.end_time.strftime('%H:%M')
                yield {"id":l, "time":k}
    
    location = request.GET.get('clinic')
    date = request.GET.get('date')
    date = datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

    time_obj = list(gen())
    response_data = {
        'times':time_obj
    }
    return JsonResponse(response_data)

def del_driver(request, slug, driver):
    company = get_object_or_404(CorporateClient, slug=slug)
    check_user(current_user=request.user, slug_user=company.user)
    driver = get_object_or_404(InternetClient, slug=driver)
    try:

        driver.delete()
        response_data = {
            'reply':'success'
        }
 
    except:

        response_data = {
            'reply':'failed'
        }
    return JsonResponse(response_data)

