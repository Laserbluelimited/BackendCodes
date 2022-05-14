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
    path('<slug>/detail', clinic_views.ClinicDetailView.as_view(), name='clinic-detail'),
    path('<slug>/edit', clinic_views.ClinicEditView.as_view(), name='clinic-edit'),
    path('<slug>/delete', clinic_views.del_clinic, name='clinic_delete'),
    path('doctor-detail/<slug>', clinic_views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctor-registration', clinic_views.DoctorRegistration.as_view(), name='doctor-registration'),
    path('doctor-list', clinic_views.DoctorListView.as_view(), name='doctor-list'),
    path('<slug>-edit/doctor', clinic_views.DoctorEditView.as_view(), name='doctor-edit'),
    path('<slug>-delete/doctor', clinic_views.del_doctor, name='doctor-delete'),
    path('doctor-sche-calendar',sche_views.DoctorScheduleCalendarView.as_view(), name='doc-sche-cal'),
    path('doctor-sche-tab', sche_views.DoctorScheduleTableView.as_view(), name="doc-sche-tab"),
    path('schedule/<slug>-edit', sche_views.ScheduleEditView.as_view(), name='doc-sche-edit'),
    path('schedule/<slug>-delete', sche_views.del_schedule, name='doc-sche-del'),
    path('doc-sche-reg', sche_views.DoctorSchedulesRegistrationView.as_view(), name='doc-sche-reg'),
    path('testing', views.TestingView.as_view(), name='testing'),
    path('add-product', prod_views.AddProductView.as_view(), name='add-product'),
    path('view-products', prod_views.ViewProductView.as_view(), name='view-product'), 
    path('product/<slug>-edit', prod_views.EditProductView.as_view(), name="product-edit"),
    path('product/<slug>-view', prod_views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<slug>-delete', prod_views.del_product, name='product-delete'),

    #client Management
    path('internet-clients-list', client_views.InternetClientTableView.as_view(), name='intrnt-cli-list'),
    path('corporate-client-list', client_views.CorporateClientTableView.as_view(), name='crprt-cli-list'),
    path('internet-client-reg', client_views.InternetClientRegistrationView.as_view(), name='intrnt-cli-reg'),
    path('corporate-client-reg', client_views.CorporateClientRegistrationView.as_view(), name='crprt-cli-reg'),
    path('crprt-client-detail/<slug>', client_views.CorporateDetailView.as_view(), name='crprt-cli-det'),
    path('int-client-detail/<slug>', client_views.InternetDetailView.as_view(), name='intrnt-cli-det'),
    path('internet-client/<slug>-edit', client_views.InternetClientEdit.as_view(), name='intrnt-cli-edit'),
    path('internet-client/<slug>-delete', client_views.del_ic, name='intrnt-cli-del'),
    path('corporate-client/<slug>-edit', client_views.CorporateClientEditView.as_view(), name='crprt-cli-edit'),
    path('corporate-client/<slug>-delete', client_views.del_cc, name='crprt-cli-del'),

    #appointment
    path('place-icorder', booking_views.ICPlaceOrderAdminView.as_view(), name='place-order'),
    path('test-order', booking_views.ICPlaceOrderView.as_view(), name='test-order'),
    path('test-checkout', csrf_exempt(booking_views.ICOrderCheckoutView.as_view()), name='test-checkout'),
    path('webhook', payment_views.my_webhook_view, name='stripe-webhook'),
    path('payment-success', payment_views.PaymentSuccessView.as_view(), name='payment-success'),
    path('payment-cancel', payment_views.PaymentCancelView.as_view(), name='payment-cancel'),
    path('icorder-list', booking_views.ICOrderTableView.as_view(), name='icorder-list'),
    path('appointment-table', booking_views.AppointmentTableView.as_view(), name='app-tab'),
    path('invoice/<slug>', booking_views.ICInvoiceView.as_view(), name='invoice'),
    path('appointment-calendar', booking_views.AppointmentCalendarView.as_view(), name='app-cal'),
    path('appointment/ajax/filter-dates', booking_views.getDates, name='ajax-dates'),
    path('appointment/ajax/filter-times', booking_views.getTimes, name="ajax-times"),

    #email
    path('email-home', email_views.EmailHomeView.as_view(), name='email-home'),
    path('email-create', email_views.CreateEmailView.as_view(), name='email-create'),
    path('email-edit/<slug>', email_views.EditEmailView.as_view(), name='email-edit')



]