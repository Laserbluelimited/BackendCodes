from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView,PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


app_name = 'authentication'

urlpatterns = [
    # Authentication
    #Viewscreen 1
    path('login',views.AuthLoginView.as_view(),name ='authlogin'),
    path('logout/', views.AuthLogoutView.as_view(), name='authlogout'),

]