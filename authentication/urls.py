from django.urls import path
from . import views


app_name = 'authentication'

urlpatterns = [
    # Authentication
    #Viewscreen 1
    path('login',views.AuthLoginView.as_view(),name ='authlogin'),
    path('logout/', views.AuthLogoutView.as_view(), name='authlogout'),

]