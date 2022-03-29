from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt


from . import views
from clinic_mgt import views as clinic_views
from prod_mgt import views as prod_views
from schedules import views as sche_views
from client_mgt import views as client_views
from booking import views as booking_views
from payment import stripe as payment_views
from e_mail import views as email_views

app_name='portal'

urlpatterns = [
    path('', views.AdminDashboardPageView.as_view(), name='dashboard'),
    path('clinic-list', clinic_views.ClinicListView.as_view(), name='clinic-list'),
    path('clinic-registration', clinic_views.ClinicRegistration.as_view(), name='clinic-registration'),
    path('doctor-detail/<slug>', clinic_views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctor-registration', clinic_views.DoctorRegistration.as_view(), name='doctor-registration'),
    path('doctor-list', clinic_views.DoctorListView.as_view(), name='doctor-list'),
    path('doctor-sche-calendar',sche_views.DoctorScheduleCalendarView.as_view(), name='doc-sche-cal'),
    path('doctor-sche-tab', sche_views.DoctorScheduleTableView.as_view(), name="doc-sche-tab"),
    path('doc-sche-reg', sche_views.DoctorSchedulesRegistrationView.as_view(), name='doc-sche-reg'),
    path('testing', views.TestingView.as_view(), name='testing'),
    path('add-product', prod_views.AddProductView.as_view(), name='add-product'),
    path('view-products', prod_views.ViewProductView.as_view(), name='view-product'), 
    path('product/<slug>', prod_views.ProductDetailView.as_view(), name='product-detail'),

    #client Management
    path('internet-clients-list', client_views.InternetClientTableView.as_view(), name='intrnt-cli-list'),
    path('corporate-client-list', client_views.CorporateClientTableView.as_view(), name='crprt-cli-list'),
    path('internet-client-reg', client_views.InternetClientRegistrationView.as_view(), name='intrnt-cli-reg'),
    path('corporate-client-reg', client_views.CorporateClientRegistrationView.as_view(), name='crprt-cli-reg'),
    path('crprt-client-detail/<slug>', client_views.CorporateDetailView.as_view(), name='crprt-cli-det'),
    path('int-client-detail/<slug>', client_views.InternetDetailView.as_view(), name='intrnt-cli-det'),

    #appointment
    path('place-icorder', booking_views.ICPlaceOrderAdminView.as_view(), name='place-order'),
    path('test-order', booking_views.ICPlaceOrderView.as_view(), name='test-order'),
    path('test-checkout', csrf_exempt(booking_views.ICOrderCheckoutView.as_view()), name='test-checkout'),
    path('webhook', payment_views.my_webhook_view, name='stripe-webhook'),
    path('payment-success', payment_views.PaymentSuccessView.as_view(), name='payment-success'),
    path('payment-success', payment_views.PaymentCancelView.as_view(), name='payment-cancel'),
    path('icorder-list', booking_views.ICOrderTableView.as_view(), name='icorder-list'),
    path('appointment-table', booking_views.AppointmentTableView.as_view(), name='app-tab'),
    path('appointment-calendar', booking_views.AppointmentCalendarView.as_view(), name='app-cal'),
    path('appointment/ajax/filter-dates', booking_views.getDates, name='ajax-dates'),
    path('appointment/ajax/filter-times', booking_views.getTimes, name="ajax-times"),

    #email
    path('email-home', email_views.EmailHomeView.as_view(), name='email-home'),
    path('email-create', email_views.CreateEmailView.as_view(), name='email-create'),
    path('email-edit/<slug>', email_views.EditEmailView.as_view(), name='email-edit')



]