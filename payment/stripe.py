import os
from urllib import request
import stripe
from skote.settings import STRIPE_API_KEY
from django.shortcuts import redirect, render
from booking.models import ICOrders, Cart, ICInvoice
from payment.models import Payment
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


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
            'quantity':cart_id.get_quantity(),
            
        }],
        mode = 'payment',
        success_url = DOMAIN+'/portal/payment-success',
        cancel_url = DOMAIN+'/portal/payment-cancel',
        metadata={
            'cart_id':cart_id.cart_id,
            }
    )
    print (session.url)

    return redirect(session.url)


class PaymentSuccessView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='payment/success.html'

    def get(self, request):
        if 'cart_id' in request.session:
            del request.session['cart_id']
            request.session.modified = True
        return render(request, self.template_name)

class PaymentCancelView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='payment/cancel.html'

    def get(self, request):
        return render(request, self.template_name)

@csrf_exempt
def my_webhook_view(request):
    endpoint_secret = 'whsec_5c4098fbabd6391cfcf8e92d94a4a070c70ec8dc1cd5f60bb8b98b39ec62bf23'
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        #invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        #invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        #fulfill the purchase..
        fulfill_order(session)

    return HttpResponse(200)

def fulfill_order(session):
    session_id = session['id']

    session_object = stripe.checkout.Session.retrieve(session_id)
    
    if 'cart_id' in session_object['metadata']:

        #get cart id
        #create order, payment and invoice object
        #update appointment status, update client status, update time slot status

        cart = Cart.objects.get(cart_id=session_object['metadata']['cart_id'])
        order_obj = ICOrders.objects.create(client=cart.client, appointment=cart.appointment, product=cart.product, total_price=session_object['amount_total'], payment_status=session_object['payment_status'], order_medium='website', payment_medium='stripe')
        payment_obj = Payment.objects.create(order_id=order_obj.order_number, stripe_session_id=session_id, status=session_object['payment_status'], total_amount=session_object['amount_total'])
        invoice=ICInvoice.objects.create(order_id=order_obj.id, payment_id=payment_obj.id)

        if session_object['payment_status']=='paid':
            cart.appointment.update_status(1)
            cart.client.update_status(1)
            cart.appointment.time_slot.update_status(2)

            #send email
        
        else:
            cart.appointment.time_slot.update_status(0)
            cart.appointment.delete()
            print('unpaid')

    print('fulfilling order')