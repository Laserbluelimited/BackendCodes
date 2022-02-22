from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView,PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import MyPasswordSetView ,MyPasswordChangeView




urlpatterns = [
    # Authentication
    #Viewscreen 1
    path('login',views.AuthLoginView.as_view(),name ='authlogin'),
    path('register',views.AuthRegisterView.as_view(),name ='authregister'),
    path('lock-screen',views.AuthLockScreenView.as_view(),name ='authlockscreen'),
    path('authrecoverpw',views.AuthRecoverpwView.as_view(),name ='authrecoverpw'),
    path('change-password',views.AuthChangePasswordView.as_view(),name ='passwordchange'),
    path('confirm-mail',views.AuthConfirmMailView.as_view(),name ='confirmmail'),
    path('email-verificaton',views.AuthEmailVerificationView.as_view(),name ='emailverificaton'),

    #allauth
    path('logout/',TemplateView.as_view(template_name="account/logout-success.html"),name ='pages-logout'),
    path('lockscreen/',TemplateView.as_view(template_name="account/lock-screen.html"),name ='pages-lockscreen'),
    #Custum change password done page redirect
    path('accounts/password/change/', login_required(MyPasswordChangeView.as_view()), name="account_change_password"),
    #Custum set password done page redirect
    path('accounts/password/set/', login_required(MyPasswordSetView.as_view()), name="account_set_password"),
    path('auth-two-step-verificaton',views.AuthTwoStepVerificationView.as_view(),name ='twostepverification'),
]