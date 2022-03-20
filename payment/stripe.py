import os
import stripe
from skote.settings import STRIPE_API_KEY
from django.shortcuts import redirect, render
from booking.forms import CartForm
from django.views import View
from booking.models import Cart



stripe.api_key = STRIPE_API_KEY
DOMAIN = 'http://localhost:8000'

def iccheckout_stripe(cart_id):
    print('hi')
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency':'usd',
                'product_data': {
                    'name':cart_id.get_product()
                },
                'unit_amount':55
            },
            'quantity':cart_id.get_quantity()
        }],
        mode = 'payment',
        success_url = DOMAIN+'/portal/payment-success',
        cancel_url = DOMAIN+'/portal/payment-cancel',
    )
    print (session.url)

    return redirect(session.url)


class PaymentSuccessView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='payment/success.html'

    def get(self, request):
        return render(request, self.template_name)

class PaymentCancelView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='payment/cancel.html'

    def get(self, request):
        return render(request, self.template_name)
