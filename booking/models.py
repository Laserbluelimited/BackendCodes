from venv import create
from django.db import models
import datetime

# Create your models here.

class Appointment(models.Model):
    id = models.IntegerField('appointment_id', primary_key=True)
    doctor = models.ForeignKey('clinic_mgt.Doctor', on_delete=models.CASCADE)
    clinic = models.ForeignKey('clinic_mgt.Clinic', on_delete=models.CASCADE)
    client = models.ForeignKey('client_mgt.InternetClient', on_delete=models.CASCADE)
    date = models.DateField('date', null=True)
    day_of_week = models.CharField('day_of_week', max_length=10, null=True)
    start_time = models.TimeField('actual_start_time', null=True)
    end_time = models.TimeField('actual_end_time', null=True)
    notes = models.TextField('notes', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.start_time) + ' ' + str(self.doctor)
    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

        
    def get_day_of_week(self):
        return self.day_of_week

    def get_date(self):
        return self.date

    def get_doctor(self):
        return self.doctor

    def get_clinic(self):
        return self.clinic


    def get_start_moment(self):
        return self.start_time.isoformat()

    def get_end_moment(self):
        return self.end_time.isoformat()
    

    def save(self, *args, **kwargs):
        self.day_of_week = self.date.strftime('%A')
        self.end_time = (datetime.datetime.combine(datetime.date.today(), self.start_time)+datetime.timedelta(minutes=15)).time()
        return super(Appointment,self).save(*args, **kwargs)


class ICOrders(models.Model):
    id = models.IntegerField('order_id', primary_key=True)
    order_number = models.IntegerField('order_number', null=True)
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
