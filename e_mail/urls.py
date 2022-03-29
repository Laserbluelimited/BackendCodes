from django.urls import path
from . import views

app_name = 'e_mail'

urlpatterns = [
    path('email-home', views.EmailHomeView.as_view, name='email-home')
]