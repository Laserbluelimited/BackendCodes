from django.urls import path
from . import views
from booking import views as booking_views
from client_mgt import views as client_mgt_views

app_name='display'


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('about', views.AboutPageView.as_view(), name="about-page"),
    path('location', views.LocationPageView.as_view(), name='location-page'),
    path('hgvmedical', views.HgvPageView.as_view(), name='hgv'),
    path('pvcmedical', views.PvcPageView.as_view(), name='pvc'),
    path('taximedical', views.TaxiPageView.as_view(), name='taxi'),
    path('other-medical-services', views.OtherServicesPageView.as_view(), name='other'),
    # path('contact-us', views.ContactUsPageView.as_view(), name='contact-us'),
    path('business/', views.BusinessClientsPageView.as_view(), name='business-clients'),

    #booking
    path('book-appointment', booking_views.ICPlaceOrderWebView.as_view(), name='booking'),
    path('checkout', booking_views.ICOrderWebCheckoutView.as_view(), name='checkout'),
    path('booking/ajax/filter-dates', views.getDates, name='ajax-dates'),
    path('booking/ajax/filter-times', views.getTimes, name="ajax-times"),
    path('business/application', client_mgt_views.CorporateClientRegistrationWebView.as_view(), name='bus-application'),
    path('business/dashboard', views.CorporateDashboardView.as_view(), name='dashboard'),
]