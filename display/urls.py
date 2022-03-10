from django.urls import path
from . import views

app_name='display'


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('about', views.AboutPageView.as_view(), name="about-page"),
    path('location', views.LocationPageView.as_view(), name='location-page')
]