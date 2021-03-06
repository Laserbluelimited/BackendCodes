import stripe
from skote.settings import STRIPE_API_KEY
from django.shortcuts import redirect, render
from booking.models import ICOrders, Cart, ICInvoice, CCOrders, CCart, CCInvoice, CorporateAppointment
from payment.models import Payment
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from client_mgt.models import CorporateClient
from e_mail import send


stripe.api_key = STRIPE_API_KEY


# DOMAIN='http://127.0.0.1:8000' 
DOMAIN='http://13.40.3.25'



#<<<===============================================================Internet Orders===============================================================================================>>>
#internet order stripe checkout client

def iccheckout_stripe(cart_id):
    session = stripe.checkout.Session.create(
        customer_email= cart_id.get_email(),
        line_items=[{
            'price_data': {
                'currency':'usd',
                'product_data': {
                    'name':cart_id.get_product()
                },
                'unit_amount':int(cart_id.get_price()*100)
            },
            'quantity':cart_id.get_quantity(),
            
        }],
        mode = 'payment',
        success_url = DOMAIN+'/payment/payment-success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = DOMAIN+'/payment/payment-cancel',
        metadata={
            'cart_id':cart_id.cart_id,
            }
    )

    return redirect(session.url)

#internet client fulfill order

def fulfill_order(session):
    session_id = session['id']

    session_object = stripe.checkout.Session.retrieve(session_id)
    
    if 'cart_id' in session_object['metadata']:

        #get cart id
        #create order, payment and invoice object
        #update appointment status, update client status, update time slot status

        cart = Cart.objects.get(cart_id=session_object['metadata']['cart_id'])
        order_obj = ICOrders.objects.create(client=cart.client, appointment=cart.appointment, product=cart.product, total_price=session_object['amount_total'], payment_status=session_object['payment_status'], order_medium='website', payment_medium='stripe', cart=cart, coupon=cart.coupon)
        payment_obj = Payment.objects.create(order_id=order_obj.order_number, stripe_session_id=session_id, status=session_object['payment_status'], total_amount=session_object['amount_total'])
        invoice=ICInvoice.objects.create(order_id=order_obj.id, payment_id=payment_obj.id)
        session_object['metadata']['order_obj']=order_obj.order_number

        if session_object['payment_status']=='paid':
            cart.appointment.update_status(1)
            cart.client.update_status(1)
            cart.appointment.time_slot.update_status(2)
            cart.save()
 
            #send email
            send_mail = send.SendgridClient(session_object['customer_email'])
            send_mail.set_template_id('d-e9b30a0fdeea4643ab2ce254c6fdffe5')
            send_mail.set_template_data({'order_number':order_obj.order_number, 'address':order_obj.appointment.time_slot.schedule.clinic.address, 
            'city':order_obj.appointment.time_slot.schedule.clinic.city, 'postal_code':order_obj.appointment.time_slot.schedule.clinic.postal_code, 'first_name':order_obj.client.first_name,
            'date':str(order_obj.appointment.get_date()), 'time':str(order_obj.appointment.get_start_time()), 'product':order_obj.get_product(),
             'doctor_name':order_obj.appointment.get_doctor(), 'actual_price':str(order_obj.product.price), 'discount_value':str(((order_obj.product.price*100)-session_object['amount_total'])/100),
             'price':(session_object['amount_total']/100)})
            send_mail.send()

            #delete cart
        
        else:
            cart.appointment.time_slot.update_status(0)
            cart.save()

#webhook
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

#<=========================================CORPORATE CLIENT=======================================================================================>


#corporate client stripe checkout client

def cccheckout_stripe(cart_id):
    session = stripe.checkout.Session.create(
        customer_email= cart_id.get_email(),
        line_items=[{
            'price_data': {
                'currency':'usd',
                'product_data': {
                    'name':"Compliance Medical Appointments"
                },
                'unit_amount':int((cart_id.get_price*100)/(cart_id.get_quantity()))
            },
            'quantity':cart_id.get_quantity(),
            
        }],
        mode = 'payment',
        success_url = DOMAIN+'/payment/'+'payment-success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = DOMAIN +'/payment/'+'payment-cancel',
        metadata={
            'cart_id':cart_id.cart_id,
            'corporate':True,
            }
    )

    return redirect(session.url)

#webhook
@csrf_exempt
def my_corporate_webhook_view(request):
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
        fulfill_corporate_order(session)

    return HttpResponse(200)

#corporate client fulfill order

def fulfill_corporate_order(session):
    session_id = session['id']

    session_object = stripe.checkout.Session.retrieve(session_id)
    
    if 'cart_id' in session_object['metadata']:

        #get cart id
        #create order, payment and invoice object
        #update appointment status, update client status, update time slot status

        cart = CCart.objects.get(cart_id=session_object['metadata']['cart_id'])
        app_obj = CorporateAppointment.objects.filter(appointment_no=cart.appointment)
        order_no = increment_order_number()
        order_obj = CCOrders.objects.create(order_number=order_no, c_client=cart.client,d_client=i.client,quantity=cart.quantity, appointment=cart.appointment, total_price=session_object['amount_total'], payment_status=session_object['payment_status'], order_medium='website', payment_medium='stripe', coupon=cart.coupon)
        payment_obj = Payment.objects.create(order_id=order_no, stripe_session_id=session_id, status=session_object['payment_status'], total_amount=session_object['amount_total'])
        invoice=CCInvoice.objects.create(order=order_no, payment=payment_obj)

        if session_object['payment_status']=='paid':
            app_obj = CorporateAppointment.objects.filter(appointment_no=cart.appointment)
            for i in app_obj:

                i.update_status(1)
                i.client.update_status(1)
                i.time_slot.update_status(2)
                i.save()

            #send email
            #delete cart
        else:
            app_obj = CorporateAppointment.objects.filter(appointment_no=cart.appointment)
            for i in app_obj:
                i.time_slot.update_status(0)
                i.save()

#<===============================================COMMON PAYMENT VIEWS AND FUNCTIONS==================================================================>


class PaymentSuccessView(View):
    template_name ='payment/success.html'

    def get(self, request):
        session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
        session_id = request.GET.get('session_id')         
        payment_status = session['payment_status']
        print(payment_status)
        email = session['customer_email']
        message = 'yes'
        if 'cart_id' in request.session:
            del request.session['cart_id']
            request.session.modified = True
        if  'corporate' in session['metadata']:
            company = CorporateClient.objects.get(main_contact_email=email)
        if 'cor_cart_id' in request.session:
            del request.session['cor_cart_id']
            request.session.modified = True
            return render(request, self.template_name, context={'message':message,'session_id':session_id, 'payment_status':payment_status, 'email':email, 'company':company})

        return render(request, self.template_name, context={'message':message, 'payment_status':payment_status, 'email':email,'session_id':session_id})


def resend_email(self, request):
    if request.GET.get('session_id'):
        session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))            
        payment_status = session['payment_status']
        email = session['customer_email']
        order_obj = ICOrders.objects.get(order_number=session['metadata']['order_obj'])
        send_mail = send.SendgridClient(email)
        send_mail.set_template_id('d-e9b30a0fdeea4643ab2ce254c6fdffe5')
        send_mail.set_template_data({'order_number':order_obj.order_number, 'address':order_obj.appointment.time_slot.schedule.clinic.address, 
        'city':order_obj.appointment.time_slot.schedule.clinic.city, 'postal_code':order_obj.appointment.time_slot.schedule.clinic.postal_code, 'first_name':order_obj.client.first_name,
        'date':str(order_obj.appointment.get_date()), 'time':str(order_obj.appointment.get_start_time()), 'product':order_obj.get_product(),
            'doctor_name':order_obj.appointment.get_doctor(), 'actual_price':str(order_obj.product.price), 'discount_value':str(((order_obj.product.price*100)-session_object['amount_total'])/100),
            'price':(session['amount_total']/100)})
        send_mail.send()
        

    message = 'yes'
    if 'cart_id' in request.session:
        del request.session['cart_id']
        request.session.modified = True
    if  'corporate' in session['metadata']:
        company = CorporateClient.objects.get(main_contact_email=email)
    if 'cor_cart_id' in request.session:
        del request.session['cor_cart_id']
        request.session.modified = True
        return render(request, 'payment/success.html', context={'message':message, 'payment_status':payment_status, 'email':email, 'company':company})

    return render(request, 'payment/success.html', context={'message':message, 'payment_status':payment_status, 'email':email})

class PaymentCancelView(View):
    login_url = '/auth/login'
    redirect_field_name = 'redirect_to'
    template_name ='payment/cancel.html'

    def get(self, request):
        return render(request, self.template_name)

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
