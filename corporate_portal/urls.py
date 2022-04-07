from django.urls import path, include
from . import views


app_name = 'corporate_portal'

urlpatterns = [
    path('login', views.AuthLoginView.as_view(), name='login'),
    path('<slug>/dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('<slug>/add-drivers', views.AddDriverView.as_view(), name='add-driver'),
]