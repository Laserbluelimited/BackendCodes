from django.urls import path
from . import views
from clinic_mgt import views as clinic_views


app_name='portal'

urlpatterns = [
    path('', views.AdminDashboardPageView.as_view(), name='dashboard'),
    path('clinic-list', clinic_views.ClinicListView.as_view(), name='clinic-list'),
    path('clinic-registration', clinic_views.ClinicRegistration.as_view(), name='clinic-registration'),
    path('doctor-registration', clinic_views.DoctorRegistration.as_view(), name='doctor-registration'),
    path('doctor-list', clinic_views.DoctorListView.as_view(), name='doctor-list'),
    path('doctor-sche-calendar/<int:url_para>', clinic_views.DoctorSchedules.as_view(), name='doc-sche-cal'),
    path('doctor-sche-tab/<int:url_para>', clinic_views.ViewSchedule.as_view(), name="doc-sche-tab"),
    path('doc-sche-reg/<int:url_para>', clinic_views.DoctorSchedulesRegistration.as_view(), name='doc-sche-reg'),
    path('testing', views.TestingView.as_view(), name='testing')

]