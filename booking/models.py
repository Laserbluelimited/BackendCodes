from ast import mod
from django.db import models

# Create your models here.

def increment_app_id():
    last_app = Appointment.objects.all().order_by('id').last()
    if not last_app:
        return 'DMAPP0000001'
    app_id = last_app.appointment_id
    app_int = int(app_id.split('DMAPP')[-1])
    width = 7
    new_app_int = app_int + 1
    formatted = (width - len(str(new_app_int))) * "0" + str(new_app_int)
    new_app_no = 'DMAPP' + str(formatted)
    return new_app_no  



def increment_invoice_number():
    last_invoice = ICInvoice.objects.all().order_by('id').last()
    if not last_invoice:
        return 'DMINV0000001'
    invoice_no = last_invoice.invoice_number
    invoice_int = int(invoice_no.split('DMINV')[-1])
    width = 7
    new_invoice_int = invoice_int + 1
    formatted = (width - len(str(new_invoice_int))) * "0" + str(new_invoice_int)
    new_invoice_no = 'DMINV' + str(formatted)
    return new_invoice_no  



def increment_ico_id():
    last_ico = ICOrders.objects.all().order_by('id').last()
    if not last_ico:
        return 'DMICO0000001'
    ico_id = last_ico.order_number
    ico_int = int(ico_id.split('DMICO')[-1])
    width = 7
    new_ico_int = ico_int + 1
    formatted = (width - len(str(new_ico_int))) * "0" + str(new_ico_int)
    new_ico_no = 'DMICO' + str(formatted)
    return new_ico_no  





class Appointment(models.Model):
    id = models.IntegerField('appointment_id', primary_key=True)
    appointment_id = models.CharField('appointment_id', max_length=20, default=increment_app_id)
    client = models.ForeignKey('client_mgt.InternetClient', on_delete=models.CASCADE)
    time_slot = models.OneToOneField('schedules.Timeslots', on_delete=models.CASCADE)
    notes = models.TextField('notes', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField('status', max_length=20, choices=[(0, 'not paid'), (1, 'paid')])

    def __str__(self):
        return str(self.time_slot.schedule.start_time) + ' ' + str(self.time_slot.schedule.doctor)

    def update_status(self, status):
        self.status = status
        self.save()


    def get_start_time(self):
        return self.time_slot.schedule.start_time

    def get_end_time(self):
        return self.time_slot.schedule.end_time
    

        
    def get_day_of_week(self):
        return self.time_slot.schedule.day_of_week

    def get_date(self):
        return self.time_slot.schedule.date

    def get_doctor(self):
        return self.time_slot.schedule.doctor

    def get_clinic(self):
        return self.time_slot.schedule.clinic


    def get_start_moment(self):
        return self.time_slot.schedule.start_time.isoformat()

    def get_end_moment(self):
        return self.time_slot.schedule.end_time.isoformat()
    


#internet client orders
class ICOrders(models.Model):
    id = models.AutoField('order_id', primary_key=True)
    order_number = models.CharField('order_number', max_length=20, default=increment_ico_id)
    client = models.ForeignKey('client_mgt.InternetClient', on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    product = models.ForeignKey('prod_mgt.Product', on_delete=models.CASCADE)
    placed_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField('quantity', default=1)
    total_price = models.IntegerField('total_price')
    payment_status = models.CharField('payment_status', max_length=30, choices=[('failed', 'failed'),('refund', 'refund'),('success','success'), ('pending', ('pending'))])
    order_medium = models.CharField('order_medium', max_length=30, choices=[('portal','portal'),('website','website')])
    payment_medium = models.CharField('payment_medium', max_length=30, choices=[('stripe','stripe'),('transfer','transfer')])
    fulfilled = models.BooleanField('fulfilled', default=False)


    def save(self, *args, **kwargs):
        self.total_price = self.quantity*self.product.price
        return super(ICOrders,self).save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    def get_id(self):
        return self.id

    def get_order_number(self):
        return self.order_number

    def get_appointment(self):
        return self.appointment
    
    def get_product(self):
        return self.product

    def get_client(self):
        return self.client

    def get_date_placed(self):
        return self.placed_at

    def get_quantity(self):
        return self.quantity

    def get_total_price(self):
        return self.total_price

    def get_payment_status(self):
        return self.payment_status

    def get_order_medium(self):
        return self.order_medium

    def get_payment_medium(self):
        return self.payment_medium

    def get_fulfilled(self):
        return self.fulfilled



class Cart(models.Model):
    cart_id = models.CharField('cart_id', primary_key=True, max_length=100)
    client = models.ForeignKey('client_mgt.InternetClient', on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    product = models.ForeignKey('prod_mgt.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=1)

    def __str__(self):
        return self.cart_id

    def get_quantity(self):
        return self.quantity

    def get_product(self):
        return self.product.name_of_prod

    def get_name(self):
        return self.client.first_name + ' ' + self.client.last_name

    def get_date(self):
        return self.appointment.time_slot.schedule.date

    def get_location(self):
        return self.appointment.time_slot.schedule.clinic.address

    def get_price(self):
        return self.product.price


class ICInvoice(models.Model):
    id = models.IntegerField('id', primary_key=True)
    invoice_number = models.CharField('invoice_number', max_length=20, default=increment_invoice_number)
    order = models.OneToOneField('ICOrders', on_delete=models.CASCADE)
    payment = models.OneToOneField('payment.Payment', on_delete=models.CASCADE)
    issued_at = models.DateTimeField('issued_at', auto_now_add=True)

    def __str__(self):
        return self.invoice_number

    def get_issued_at(self):
        return self.issued_at

    def get_client(self):
        return self.order.client

    def get_product(self):
        return self.order.product

    def get_price(self):
        return self.order.total_price

    def get_product(self):
        return self.order.product

    def get_payment(self):
        return self.payment
