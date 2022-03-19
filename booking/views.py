from django import views
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from schedules.models import ScheduleDates
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrderForm, CartForm
from .models import Appointment, ICOrders
import datetime
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
def book_appointment(model, schedule, client, status=0, notes=None):

    """
    This function basically helps to book an appointment
    model: Appointment model
    schedule: schedule object/instance
    client: internet client object/instance
    status: 0 if it has not been paid for, 1 if it has been paid for

    if status is 0, it updates the schedule object to 1(temporarily unavailable)
    if status is 1, it updates the schedule object to 2(has been paid for)
    
    
    """
    app_obj = model.objects.create(id=id_increment(Appointment, 114000), schedule=schedule, client=client, status=status, notes=notes )
    if status == 0:
        schedule.status = 1
        schedule.save()
    elif status == 1:
        schedule.status = 2
        schedule.save()
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
            sche_obj = ScheduleDates.objects.get(id=time_slot)

            #book appointment
            app_obj = book_appointment(Appointment, schedule=sche_obj, client=client, status=1)

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
    template_name ='orders/order-form.html'
    form_class = CartForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            #if form is valid, do the following
            #1. save individual client
            #2. book appointment
            #3. add to cart
            #4. add cart id to session
            return redirect('portal:icorder-checkout')
        return render(request, self.template_name, context={'form':form})









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
            m = i.strftime("%#d-%#m-%Y")
            yield m


    location = request.GET.get('clinic')
    dates = ScheduleDates.objects.filter(clinic=location, status=0).values_list('date', flat=True).distinct()
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
        for i in ScheduleDates.objects.filter(date=date, clinic=location, status=0):
            l=i.id
            k =i.start_time.strftime('%H:%M') + ' - ' + i.end_time.strftime('%H:%M')
            yield {"id":l, "time":k}
    
    location = request.GET.get('clinic')
    date = request.GET.get('date')
    date = datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

    time_obj = list(gen())
    response_data = {
        'times':time_obj
    }
    return JsonResponse(response_data)


