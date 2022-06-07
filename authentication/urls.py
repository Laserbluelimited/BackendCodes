from django.urls import path
from . import views


app_name = 'authentication'

urlpatterns = [
    # Authentication
    #Viewscreen 1
    path('login',views.AuthLoginView.as_view(),name ='authlogin'),
    path('logout/', views.AuthLogoutView.as_view(), name='authlogout'),
    path('cor/activate/<uidb64>/<token>', views.activate_cor_user, name='activate_cor_user'),
    path('cor/<slug>/send_password_mail', views.send_cor_password_mail, name='send-cor-pass-mail')

]