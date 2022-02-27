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
]