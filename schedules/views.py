from email import message
from multiprocessing import context
from pydoc import doc
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DoctorScheduleForm, ScheduleUploadForm
from .models import ScheduleDates
import datetime
# Create your views here.
class DoctorScheduleCalendarView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='schedule/calendar-actual.html'    
    def get(self, request):
        schedules = ScheduleDates.objects.all()

        return render(request, self.template_name, context={'schedules':schedules})

class DoctorScheduleTableView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='schedule/doctor-schedule-table.html' 
    def get(self, request):
        schedules = ScheduleDates.objects.all()
        return render(request, self.template_name, context={'schedules':schedules})

class DoctorSchedulesRegistrationView(LoginRequiredMixin, View):
    login_url = '/auth/login'
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



            def gen_time_slots(start, end):
                a = start
                
                while a <=end:
                    e = (datetime.datetime.combine(datetime.date.today(), a)+datetime.timedelta(minutes=15)).time()
                    duration = datetime.datetime.combine(date.min, end_time) - datetime.datetime.combine(date.min, start_time)
                    yield ScheduleDates(start_time=a, end_time=e, clinic=clinic, doctor=doctor, date=date, duration=duration, day_of_week=date.strftime('%A') )
                    a = e
                    
            
            slots = list(gen_time_slots(start_time, end_time))
            ScheduleDates.objects.bulk_create(slots)

            return redirect('portal:doc-sche-tab')
        return render(request, self.template_name, context={'form':form})


# def import_data(request):
#     if request.method == "POST":
#         upload_form = ScheduleUploadForm(request.POST, request.FILES)

#         def sche_func(row):
#             q = Doctor.objects.get(name=row[0])
#             a = Clinic.objects.get(name=row[1])

#             row[0] = q
#             row[1] = a
#             return row

#         if upload_form.is_valid():
#             request.FILES["file"].save_book_to_database(
#                 model = ScheduleDates,
#                 initializers=[None, choice_func],
#                 mapdicts=[
#                     ["question_text", "pub_date", "slug"],
#                 ],
#             )
#             return redirect("handson_view")
#         else:
#             return HttpResponseBadRequest()