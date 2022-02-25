from django.urls import path
from . import views


app_name='portal'

urlpatterns = [
    path('dashboard', views.AdminDashboardPageView.as_view(), name='dashboard'),
]