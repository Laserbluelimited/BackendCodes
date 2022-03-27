from django.urls import path
from . import views

app_name='display'


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('about', views.AboutPageView.as_view(), name="about-page"),
    path('location', views.LocationPageView.as_view(), name='location-page'),
    #booking
    path('booking', views.ICBookingView.as_view(), name='booking'),
    path('booking/coupon', views.CCouponView.as_view(), name='coupon')
    ,path('booking/service', views.CServiceView.as_view(), name='service'),
    path('booking/user', views.CUserView.as_view(), name='user'),
    path('hhhh', views.hhhhView.as_view(), name='hhhh')
]