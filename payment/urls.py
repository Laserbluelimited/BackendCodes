from django.urls import path
from . import stripe

app_name='payment'


urlpatterns = [
    path('payment-success', stripe.PaymentSuccessView.as_view(), name='payment-success'),
    path('payment-cancel', stripe.PaymentCancelView.as_view(), name='payment-cancel'),
    path('webhook', stripe.my_webhook_view, name='stripe-webhook'),
    path('corporate-webhook', stripe.my_corporate_webhook_view, name="cor-webhook")
]