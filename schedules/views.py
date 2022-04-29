from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import DoctorScheduleForm
from .models import ScheduleDates, TimeSlots
import datetime
# Create your views here.


def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id



class DoctorScheduleCalendarView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/auth/login'
    permission_required = ('schedules.change_scheduledates')
    redirect_field_name = 'redirect_to'
    template_name ='schedule/calendar-actual.html'    
    def get(self, request):
        schedules = ScheduleDates.objects.all()

        return render(request, self.template_name, context={'schedules':schedules})

class DoctorScheduleTableView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/auth/login'
    permission_required = ('schedules.change_scheduledates')
    redirect_field_name = 'redirect_to'
    template_name ='schedule/doctor-schedule-table.html' 
    def get(self, request):
        schedules = ScheduleDates.objects.all().order_by('-id')
        paginator = Paginator(schedules, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, context={'schedules':schedules, 'page_obj':page_obj})

class DoctorSchedulesRegistrationView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = '/auth/login'
    permission_required = ('schedules.change_scheduledates')
    redirect_field_name = 'redirect_to'
    template_name ='schedule/schedule-form.html'
    form_class = DoctorScheduleForm 
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form':form})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            doctor = form.cleaned_data['doctor']
            clinic = form.cleaned_data['clinic']


            schedule_obj = ScheduleDates.objects.create(id=id_increment(ScheduleDates, 2110000), start_time=start_time, end_time=end_time, clinic=clinic, doctor=doctor, date=date)
            def gen_time_slots(start, end):
                a = start
                
                while a <=end:
                    e = (datetime.datetime.combine(datetime.date.today(), a)+datetime.timedelta(minutes=15)).time()
                    duration = datetime.timedelta(minutes=15)
                    yield TimeSlots( start_time=a, end_time=e, schedule=schedule_obj, status=0, duration=duration)
                    a = e
                    
            
            slots = list(gen_time_slots(start_time, end_time))
            TimeSlots.objects.bulk_create(slots)

            return redirect('portal:doc-sche-tab')
        return render(request, self.template_name, context={'form':form})


class ScheduleEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    permission_required = ('schedules.change_scheduledates')
    template_name ='schedule/schedule-edit.html'
    form_class = DoctorScheduleForm 
    def get(self, request, slug):
        schedule = get_object_or_404(ScheduleDates, slug=slug)
        form = self.form_class()
        return render(request, self.template_name, context={'form':form, 'schedule':schedule})

    def post(self, request, slug):
        schedule = get_object_or_404(ScheduleDates, slug=slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            schedule.date = form.cleaned_data['date']
            schedule.start_time = form.cleaned_data['start_time']
            schedule.end_time = form.cleaned_data['end_time']
            schedule.doctor = form.cleaned_data['doctor']
            schedule.clinic = form.cleaned_data['clinic']

            schedule.save()

            time_slots = TimeSlots.objects.filter(schedule=schedule)
            time_slots.delete()

            def gen_time_slots(start, end):
                a = start
                while a <=end:
                    e = (datetime.datetime.combine(datetime.date.today(), a)+datetime.timedelta(minutes=15)).time()
                    duration = datetime.timedelta(minutes=15)
                    yield TimeSlots( start_time=a, end_time=e, schedule=schedule, status=0, duration=duration)
                    a = e
                    
            
            slots = list(gen_time_slots(schedule.start_time, schedule.end_time))
            TimeSlots.objects.bulk_create(slots)

            return redirect('portal:doc-sche-tab')
        return render(request, self.template_name, context={'form':form, 'schedule':schedule})


def del_schedule(request, slug):
    sche = get_object_or_404(ScheduleDates, slug=slug)
    try:

        sche.delete()
        response_data = {
            'reply':'success'
        }
 
    except:

        response_data = {
            'reply':'failed'
        }
    return JsonResponse(response_data)
