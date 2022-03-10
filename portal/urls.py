from django.urls import path
from . import views
from clinic_mgt import views as clinic_views
from prod_mgt import views as prod_views
from schedules import views as sche_views


app_name='portal'

urlpatterns = [
    path('', views.AdminDashboardPageView.as_view(), name='dashboard'),
    path('clinic-list', clinic_views.ClinicListView.as_view(), name='clinic-list'),
    path('clinic-registration', clinic_views.ClinicRegistration.as_view(), name='clinic-registration'),
    path('clinic-detail/<url_para>', clinic_views.ClinicDetailView.as_view(), name='clinic-detail'),
    path('doctor-registration', clinic_views.DoctorRegistration.as_view(), name='doctor-registration'),
    path('doctor-list', clinic_views.DoctorListView.as_view(), name='doctor-list'),
    path('doctor-sche-calendar',sche_views.DoctorScheduleCalendarView.as_view(), name='doc-sche-cal'),
    path('doctor-sche-tab', sche_views.DoctorScheduleTableView.as_view(), name="doc-sche-tab"),
    path('doc-sche-reg', sche_views.DoctorSchedulesRegistrationView.as_view(), name='doc-sche-reg'),
    path('testing', views.TestingView.as_view(), name='testing'),
    path('add-product', prod_views.AddProductView.as_view(), name='add-product'),
    path('view-products', prod_views.ViewProductView.as_view(), name='view-product'),
    path('product/<slug>', prod_views.ProductDetailView.as_view(), name='product-detail')

]