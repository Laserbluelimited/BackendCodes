from django import views
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from clinic_mgt.models import Clinic
from schedules.models import ScheduleDates, TimeSlots
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrderForm, CartForm, CartWebForm
from .models import Appointment, Cart, ICOrders
import datetime
from client_mgt.models import InternetClient
from booking import cart
from payment import stripe
# Create your views here.



#Function to increase id of any model
def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id

#function to book appointment
def book_appointment(model, time_slot, client, status=0, notes=None):

    """
    This function basically helps to book an appointment
    model: Appointment model
    schedule: time slot object/instance
    client: internet client object/instance
    status: 0 if it has not been paid for, 1 if it has been paid for

    if status is 0, it updates the schedule object to 1(temporarily unavailable)
    if status is 1, it updates the schedule object to 2(has been paid for)
    
    
    """
    app_obj = model.objects.create(id=id_increment(Appointment, 114000), time_slot=time_slot, client=client, status=status, notes=notes )
    if status == 0:
        time_slot.status = 1
        time_slot.save()
    elif status == 1:
        time_slot.status = 2
        time_slot.save()
    return app_obj




#views

class AppointmentCalendarView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='appointment/calendar-actual.html'    
    def get(self, request):
        appntments = Appointment.objects.all()

        return render(request, self.template_name, context={'appointments':appntments})



class AppointmentTableView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='orders/appointment-table.html' 
    def get(self, request):
        appntments = Appointment.objects.all()

        return render(request, self.template_name, context={'appointments':appntments})
 



class ICOrderTableView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='orders/order-list.html' 
    def get(self, request):
        orders = ICOrders.objects.all()

        return render(request, self.template_name, context={'orders':orders})



class ICPlaceOrderAdminView(LoginRequiredMixin, views.View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='orders/order-form.html'
    form_class = OrderForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            product = form.cleaned_data['product']
            time_slot = form.cleaned_data['time_slot']

            #get schedule object from time slot
            time_slot = TimeSlots.objects.get(id=time_slot)

            #book appointment
            app_obj = book_appointment(Appointment, time_slot=time_slot, client=client, status=1)

            #place order
            order_obj = form.save(commit=False)
            order_obj.appointment = app_obj
            order_obj.product = product

            #save order
            order_obj.save()

            return redirect('portal:icorder-list')


        return render(request, self.template_name, context={'form':form})



class ICPlaceOrderView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='orders/testic-order.html'
    form_class = CartForm

    def get(self, request):
        form = self.form_class()
        if "cart_id" in request.session:
            return redirect('portal:test-checkout')
        else:
            request.session.set_test_cookie()

        return render(request, self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if request.session.test_cookie_worked():
            print(form.errors)
            if form.is_valid():
                #if form is valid, do the following'
                #1. get form data
                #2. save individual client if not save already with a status of 0
                #3. get schedule object, book appointment
                #4. add to cart and add cart id to session
                #5. redirect to checkout page


                #1.
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone = form.cleaned_data['phone']
                email = form.cleaned_data['email']
                # notes = form.cleaned_data['notes']
                time_slot = form.cleaned_data['time_slot']
                product = form.cleaned_data['product']


                #2
                if InternetClient.objects.filter(email=email).exists():
                    client_obj = InternetClient.objects.get(email=email)
                else:
                    client_obj = InternetClient.objects.create(id=id_increment(InternetClient, 1120000),status=0, first_name=first_name, phone=phone, last_name=last_name, email=email)

                #3
                sche_obj = TimeSlots.objects.get(id=time_slot)
                app_obj = book_appointment(Appointment, time_slot=sche_obj, status=0, client=client_obj)

                #4
                cart.add_to_cart(request, client=client_obj, appointment=app_obj, product=product)
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                #5
                return redirect('portal:test-checkout')
        else:
            print('cookie not present')

        return render(request, self.template_name, context={'form':form})



class ICOrderCheckoutView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='orders/testic-checkout.html'

    def get(self, request):
        if "cart_id" in request.session:
            cart_id = request.session['cart_id']
            cart_obj = Cart.objects.get(cart_id=cart_id)
        else:
            return redirect('portal:test-order')
        return render(request, self.template_name, context={ 'cart':cart_obj})

    def post(self, request):
        if request.session['cart_id']:
            cart_id = request.session['cart_id']
            cart_obj = Cart.objects.get(cart_id=cart_id)
            return stripe.iccheckout_stripe(cart_id=cart_obj)
        else:
            return redirect('portal:test-order')










#ajax request

def getDates(request):

    """
    This ajax request function basically returns dates available based on a particular location.
    """
    def gen():
        """
        This generator puts the dates in the format accepted by the bootstrap datepicker
        """
        for i in dates:
            if i>= datetime.date.today():
                m = i.strftime("%d-%m-%Y")
                yield m


    location = request.GET.get('clinic')
    dates = ScheduleDates.objects.filter(clinic=location).values_list('date', flat=True).distinct()
    date_list = list(gen())
    response_data = {
        'dates':date_list
    }
    return JsonResponse(response_data)

def getTimes(request):

    """
    This ajax request function basically returns times available based on a particular location and date.
    """
    def gen():
        for i in ScheduleDates.objects.filter(date=date, clinic=location):
            for p in TimeSlots.objects.filter(schedule=i, status=0):
                if p.start_time >= datetime.datetime.now().strftime('%H:%M'):
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






#web views

class ICPlaceOrderWebView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='display/booking.html'
    form_class = CartWebForm

    def get(self, request):
        form = self.form_class()
        clinics = Clinic.objects.all()
        if "cart_id" in request.session:
            return redirect('display:checkout')
        else:
            request.session.set_test_cookie()

        return render(request, self.template_name, context={'form':form, 'clinics':clinics})

    def post(self, request):
        clinics = Clinic.objects.all()
        form = self.form_class(request.POST)
        if request.session.test_cookie_worked():
            print(form.errors)
            if form.is_valid():
                #if form is valid, do the following'
                #1. get form data
                #2. save individual client if not save already with a status of 0
                #3. get schedule object, book appointment
                #4. add to cart and add cart id to session
                #5. redirect to checkout page


                #1.
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone = form.cleaned_data['phone']
                email = form.cleaned_data['email']
                # notes = form.cleaned_data['notes']
                time_slot = form.cleaned_data['time_slot']
                product = form.cleaned_data['product']


                #2
                if InternetClient.objects.filter(email=email).exists():
                    client_obj = InternetClient.objects.get(email=email)
                else:
                    client_obj = InternetClient.objects.create(id=id_increment(InternetClient, 1120000),status=0, first_name=first_name, phone=phone, last_name=last_name, email=email)

                #3
                sche_obj = TimeSlots.objects.get(id=time_slot)
                app_obj = book_appointment(Appointment, time_slot=sche_obj, status=0, client=client_obj)

                #4
                cart.add_to_cart(request, client=client_obj, appointment=app_obj, product=product)
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                #5
                return redirect('display:checkout')
        else:
            print('cookie not present')

        return render(request, self.template_name, context={'form':form, 'clinics':clinics})

class BacktoBookingView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='display/booking.html'

    def get(self, request):
        if "cart_id" in request.session:
            del request.session['cart_id']
            return redirect('display:booking')
        else:
            return redirect('display:booking')


class ICOrderWebCheckoutView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='display/checkout.html'

    def get(self, request):
        if "cart_id" in request.session:
            cart_id = request.session['cart_id']
            cart_obj = Cart.objects.get(cart_id=cart_id)
        else:
            return redirect('display:booking')
        return render(request, self.template_name, context={ 'cart':cart_obj})
 
    def post(self, request):
        if "cart_id" in request.session:
            cart_id = request.session['cart_id']
            cart_obj = Cart.objects.get(cart_id=cart_id)
            return stripe.iccheckout_stripe(cart_id=cart_obj)
        else:
            return redirect('display:booking')



