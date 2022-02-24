from django.urls import path
from . import views


app_name='portal'

urlpatterns = [
    path('/dashboard', views.DashboardPageView.as_view(), name='dashboard'),
    # path('clinic/dashboard', views.ClinicDashboardPageView.as_view(), name='clinic-dashboard'),
    # path('admin/dashboard', views.AdminDashboardPageView.as_view(), name='admin-dashboard'),
]