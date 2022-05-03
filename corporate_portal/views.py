from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import GroupRequiredMixin
from .forms import AddDriverFormSet, LoginForm,BaseBookingFormSet, LocationForm, AppointmentForm
from client_mgt.models import InternetClient, CorporateClient
from django.forms import formset_factory
from django.http import JsonResponse
import datetime
from schedules.models import ScheduleDates, TimeSlots
from booking.models import CCart, CorporateAppointment
from . import cart
from . import stripe



#function to book appointment
def book_appointment(model, time_slot, client,c_client,product, status=0,  notes=None,):

    """
    This function basically helps to book an appointment
    model: Appointment model
    schedule: time slot object/instance
    client: internet client object/instance
    status: 0 if it has not been paid for, 1 if it has been paid for

    if status is 0, it updates the schedule object to 1(temporarily unavailable)
    if status is 1, it updates the schedule object to 2(has been paid for)
    
    
    """
    app_obj = model.objects.create( time_slot=time_slot, client=client, status=status, notes=notes, c_client=c_client, product=product )
    if status == 0:
        time_slot.status = 1
        time_slot.save()
    elif status == 1:
        time_slot.status = 2
        time_slot.save()
    return app_obj





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
    template_name = 'cor_temp/booking.html'
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        if "cor_cart_id" in request.session:
            return redirect('corporate_portal:checkout', slug=company.slug)
        else:
            request.session.set_test_cookie()
        
        l_form = LocationForm()
        d_form = formset_factory(AppointmentForm, extra=1, formset=BaseBookingFormSet)
        d_form = d_form()
        return render(request, self.template_name, context={'company':company,  'l_form':l_form, 'd_form':d_form, 'annoying':enumerate(d_form)})
        

    def post(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        l_form = LocationForm()
        d_form = formset_factory(form=AppointmentForm, extra=1, formset=BaseBookingFormSet)
        d_form = d_form(data=self.request.POST)
        
        if d_form.is_valid() and request.session.test_cookie_worked():
            quantity = 0
            for form in d_form:
                driver = form.cleaned_data['driver']
                product = form.cleaned_data['product']
                time_slot = form.cleaned_data['time_slot']

                #3
                sche_obj = TimeSlots.objects.get(id=time_slot)
                app_obj = book_appointment(CorporateAppointment, time_slot=sche_obj, status=0, client=driver, c_client=company, product=product)
                quantity+=1

                #4
            cart.add_to_cart(request, client=company, appointment=app_obj.appointment_no, quantity=quantity)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            


            
            return redirect('corporate_portal:dashboard', slug = company.slug)
        else:
            print(d_form.errors)
            print(d_form.non_form_errors())

    

        return render(request, self.template_name, context={'company':company,  'l_form':l_form, 'd_form':d_form, 'annoying':enumerate(d_form)})


class CheckoutView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = 'cor_temp/checkout.html'
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    group_required = [u'Corporate group']

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        if "cor_cart_id" in request.session:
            basket_id = request.session['cor_cart_id']
            basket = CCart.objects.get(cart_id=basket_id)
        else:
            basket = 'empty'
            return redirect('corporate_portal:booking', slug=company.slug)

        appointments = CorporateAppointment.objects.filter(appointment_no =basket.appointment)
        return render(request, self.template_name, context={'company':company, 'appointments':appointments})

    def post(self, request):
        if "cor_cart_id" in request.session:
            cart_id = request.session['cor_cart_id']
            cart_obj = CCart.objects.get(cart_id=cart_id)
            return stripe.iccheckout_stripe(cart_id=cart_obj)
        else:
            return redirect('corporate_portal:booking')
    
        
        return render(request, self.template_name, context={'company':company, 'appointments':appointments})


def getDates(request, slug):

    """
    This ajax request function basically returns dates available based on a particular location.
    """
    def gen():
        """
        This generator puts the dates in the format accepted by the bootstrap datepicker
        """
        for i in dates:
            if i>= datetime.date.today():
                m = i.strftime("%#d-%#m-%Y")
                yield m


    location = request.GET.get('clinic')
    print(location)
    dates = ScheduleDates.objects.filter(clinic=location).values_list('date', flat=True).distinct()
    date_list = list(gen())
    response_data = {
        'dates':date_list
    }
    print(dates)
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

