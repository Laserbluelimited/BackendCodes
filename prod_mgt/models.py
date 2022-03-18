from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.



class Product(models.Model):

    id = models.IntegerField('product_id',primary_key=True, unique=True)
    name_of_prod = models.CharField('name_of_product',max_length=50, unique=True)
    slug = models.SlugField(max_length=50, help_text='Unique Value for product page URL, created from name.')
    price = models.DecimalField('price', max_digits=9, decimal_places=2)
    currency = models.CharField('currency', max_length=10, default='euros')
    image = models.ImageField()
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True)
    meta_keywords = models.CharField(max_length=255, null=True, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255, null=True, help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_of_prod)
        return super(Product,self).save(*args, **kwargs)


    def __str__(self):
        return self.name_of_prod

    def get_name(self):
        return self.name_of_prod

    def get_price(self):
        return self.price

    def get_image(self):
        return self.image

    def get_description(self):
        return self.description

    def get_meta_description(self):
        return self.meta_description

    def get_meta_keywords(self):
        return self.meta_keywords



    class Meta:
        db_table ='products'
        ordering = ['-created_at']

