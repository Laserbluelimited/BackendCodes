from django.db import models

# Create your models here.

class Product(models.Model):
    db_table = 'products'
    id = models.IntegerField('product_id',primary_key=True, unique=True)
    name_of_prod = models.CharField('name_of_product',max_length=50)
    price = models.DecimalField('price', max_digits=9, decimal_places=4)
    currency = models.CharField('currency', max_length=10, default='euros')

    def __str__(self):
        return self.name_of_prod
