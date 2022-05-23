from unicodedata import name
from django.urls import path, include
from . import views
from . import stripe


app_name = 'corporate_portal'

urlpatterns = [
    path('login', views.AuthLoginView.as_view(), name='login'),
    path('<slug>/dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('<slug>/add-drivers', views.AddDriverView.as_view(), name='add-driver'),
    path('<slug>/booking', views.BookAppointmentView.as_view(), name='booking'),
    path('<slug>/appointment/ajax/filter-dates', views.getDates, name='filter-dates'),
    path('<slug>/appointment/ajax/filter-times', views.getTimes, name='filter-times'),
    path('<slug>/appointment/ajax/redeem', views.redeem_coupon, name='redeem'),

    path('<slug>/checkout', views.CheckoutView.as_view(), name='checkout'),
    path('<slug>/success',stripe.PaymentSuccessView.as_view(), name='payment-sucess' ),
    path('<slug>/cancel',stripe.PaymentCancelView.as_view(), name='payment-sucess' ),
    path('<slug>/driver-list', views.DriverListView.as_view(), name='driver-list'),
    path('<slug>/<driver>-edit', views.DriverEditView.as_view(), name='driver-edit'),
    path('<slug>/<driver>-delete', views.del_driver, name='driver-delete'),
    path('<slug>/del-cart', views.DeleteCartView.as_view(), name='cart-del'),
    path('<slug>/orders', views.OrderListView.as_view(), name='order-list'),
    path('<slug>/invoice/<order_no>',views.InvoiceView.as_view(), name='invoice'),
]

