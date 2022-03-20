from django.db import models

# Create your models here.

class Appointment(models.Model):
    id = models.IntegerField('appointment_id', primary_key=True)
    client = models.ForeignKey('client_mgt.InternetClient', on_delete=models.CASCADE)
    schedule = models.OneToOneField('schedules.ScheduleDates', on_delete=models.CASCADE)
    notes = models.TextField('notes', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField('status', max_length=20, choices=[(0, 'not paid'), (1, 'paid')])

    def __str__(self):
        return str(self.schedule.start_time) + ' ' + str(self.schedule.doctor)
    def get_start_time(self):
        return self.schedule.start_time

    def get_end_time(self):
        return self.schedule.end_time

        
    def get_day_of_week(self):
        return self.schedule.day_of_week

    def get_date(self):
        return self.schedule.date

    def get_doctor(self):
        return self.schedule.doctor

    def get_clinic(self):
        return self.schedule.clinic


    def get_start_moment(self):
        return self.schedule.start_time.isoformat()

    def get_end_moment(self):
        return self.schedule.end_time.isoformat()
    



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
        return self.appointment.schedule.date

    def get_location(self):
        return self.appointment.schedule.clinic.address

    def get_price(self):
        return self.product.price