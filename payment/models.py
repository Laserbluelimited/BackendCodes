from django.db import models











def increment_payment_id():
    last_payment = Payment.objects.all().order_by('id').last()
    if not last_payment:
        return 'DMPAY0000001'
    payment_id = last_payment.payment_id
    payment_int = int(payment_id.split('DMPAY')[-1])
    width = 7
    new_payment_int = payment_int + 1
    formatted = (width - len(str(new_payment_int))) * "0" + str(new_payment_int)
    new_payment_no = 'DMPAY' + str(formatted)
    return new_payment_no  

class Payment(models.Model):
    id = models.AutoField('id', primary_key=True)
    payment_id = models.CharField('payment_id', max_length=20, default=increment_payment_id)
    medium = models.CharField('medium', default='stripe', max_length=20)
    order_id = models.CharField('order_id', max_length=100, unique=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    stripe_session_id = models.CharField('stripe_sess_id', max_length=255)
    status = models.CharField('status', max_length=100)
    total_amount = models.CharField('total_amount', max_length=30)


    def __str__(self):
        return self.payment_id