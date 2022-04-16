from django.urls import path, include
from . import views


app_name = 'corporate_portal'

urlpatterns = [
    path('login', views.AuthLoginView.as_view(), name='login'),
    path('<slug>/dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('<slug>/add-drivers', views.AddDriverView.as_view(), name='add-driver'),
    path('<slug>/booking', views.BookAppointmentView.as_view(), name='booking'),
    path('<slug>/appointment/ajax/filter-dates', views.getDates, name='filter-dates'),
    path('<slug>/appointment/ajax/filter-times', views.getTimes, name='filter-times'),
    path('<slug>/checkout', views.CheckoutView.as_view(), name='checkout'),
]