import os
from urllib import request
import stripe
from skote.settings import STRIPE_API_KEY
from django.shortcuts import redirect, render, get_object_or_404
from booking.models import CCOrders, CCart, CCInvoice, CorporateAppointment
from payment.models import Payment
from client_mgt.models import CorporateClient
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


stripe.api_key = STRIPE_API_KEY
DOMAIN = 'http://localhost:8000'


def increment_order_number():
    last_order = CCOrders.objects.all().order_by('id').last()
    if not last_order:
        return 'DMCOR0000001'
    order_no = last_order.order_number
    order_int = int(order_no.split('DMCOR')[-1])
    width = 7
    new_order_int = order_int + 1
    formatted = (width - len(str(new_order_int))) * "0" + str(new_order_int)
    new_order_no = 'DMCOR' + str(formatted)
    return new_order_no  



def iccheckout_stripe(cart_id, slug):
    session = stripe.checkout.Session.create(
        customer_email= cart_id.get_email(),
        line_items=[{
            'price_data': {
                'currency':'usd',
                'product_data': {
                    'name':"Compliance Medical Appointments"
                },
                'unit_amount':int((cart_id.price*100)/(cart_id.get_quantity()))
            },
            'quantity':cart_id.get_quantity(),
            
        }],
        mode = 'payment',
        success_url = DOMAIN+'/business/'+slug+'/success',
        cancel_url = DOMAIN +'/business/'+slug+'/cancel',
        metadata={
            'cart_id':cart_id.cart_id,
            }
    )
    print (session.url)

    return redirect(session.url)


class PaymentSuccessView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='cor_temp/success.html'

    def get(self, request,slug):
        company = get_object_or_404(CorporateClient, slug=slug)
        if 'cor_cart_id' in request.session:
            del request.session['cor_cart_id']
            request.session.modified = True
            print(request.session['cor_cart_id'])
        return render(request, self.template_name)

class PaymentCancelView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='cor_temp/cancel.html'

    def get(self, request, slug):
        company = get_object_or_404(CorporateClient, slug=slug)
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

        cart = CCart.objects.get(cart_id=session_object['metadata']['cart_id'])
        app_obj = CorporateAppointment.objects.filter(appointment_no=cart.appointment_no)
        order_no = increment_order_number()
        for i in app_obj:
            order_obj = CCOrders.objects.create(c_client=cart.client,d_client=i.client,quantity=cart.quantity, appointment=cart.appointment, product=i.product, total_price=session_object['amount_total'], payment_status=session_object['payment_status'], order_medium='website', payment_medium='stripe')
        payment_obj = Payment.objects.create(order_id=order_no, stripe_session_id=session_id, status=session_object['payment_status'], total_amount=session_object['amount_total'])
        invoice=CCInvoice.objects.create(order_id=order_no, payment=payment_obj)

        if session_object['payment_status']=='paid':
            cart.appointment.update_status(1)
            cart.appointment.save()
            cart.client.update_status(1)
            cart.client.save()
            cart.appointment.time_slot.update_status(2)
            cart.appointment.time_slot.save()


            #send email
            #delete cart
        
        else:
            cart.appointment.time_slot.update_status(0)
            cart.appointment.delete()
            print('unpaid')

    print('fulfilling order')