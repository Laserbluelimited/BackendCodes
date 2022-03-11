from random import choices
from xml.parsers.expat import model
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
TITLE_CHOICES = (
    ('miss', 'Miss'),
    ('mr', 'Mr.'),
    ('mrs', 'Mrs.'),
)

GENDER_CHOICES = (
    ('agender', 'Agender'),
    ('androgyne', 'Androgyne'),
    ('gender_fluid', 'Gender Fluid'),
    ('male', 'Male'),
    ('non_binary', 'Non Binary'),
    ('transgender', 'Transgender'),
    ('female', 'Female'),
)

COMPANY_TYPE_CHOICES =(
    ('miss', 'Miss'),
    ('mr', 'Mr.'),
    ('mrs', 'Mrs.'),
)
PREFERRED_MODE_CHOICES =  (
    ('agender', 'Agender'),
    ('androgyne', 'Androgyne'),
    ('gender_fluid', 'Gender Fluid'),
    ('male', 'Male'),
    ('non_binary', 'Non Binary'),
    ('transgender', 'Transgender'),
    ('female', 'Female'),
)

class InternetClient(models.Model):



    id = models.IntegerField('client_id', unique=True, primary_key=True)
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    title = models.CharField('title', max_length=20, choices=TITLE_CHOICES, null=True)
    phone = models.IntegerField('phone_number', unique=True)
    dob = models.DateField('date_of_birth')
    gender = models.CharField('gender', choices=GENDER_CHOICES, max_length=50)
    address = models.CharField('address', max_length=255)
    city = models.CharField('city', max_length=100)
    long = models.DecimalField('longitude', max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField('latitude', max_digits=9, decimal_places=6, null=True)
    postal_code = models.CharField('postal_code', max_length=20)
    country = models.CharField('country', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'internet_client'

    def __str__(self):
        return self.title + ' ' + self.user.first_name + self.user.last_name

    def get_name(self):
        return self.title + ' ' + self.user.first_name + self.user.last_name

    def get_phone(self):
        return self.phone

    def get_dob(self):
        return self.dob

    def get_city(self):
        return self.city

    def get_postal_code(self):
        return self.postal_code

    def get_address(self):
        return self.address

    def get_gender(self):
        return self.gender


class CorporateClient(models.Model):


    id = models.IntegerField('corporate_client_id', primary_key=True, unique=True)
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    company_name = models.CharField('company_name', unique=True, max_length=255)
    slug = models.SlugField(max_length=255, help_text='Unique Value for product page URL, created from name.')
    company_type = models.CharField('company_type', max_length=50, choices=COMPANY_TYPE_CHOICES)
    nature_of_business = models.CharField('nature_of_business', max_length=255, null=True)
    industry_sector = models.CharField('industry_sector', max_length=100)
    vat_reg_no = models.CharField('vat_reg_no', max_length=255)
    main_contact_number = models.CharField('company_phone', max_length=20, unique=True)
    main_contact_email = models.EmailField('company_email', unique=True)
    no_of_employees = models.IntegerField('no_of_employees')
    no_of_years = models.IntegerField('no_years_of_trade')
    address = models.CharField('address', max_length=255)
    city = models.CharField('city', max_length=100)
    long = models.DecimalField('longitude', max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField('latitude', max_digits=9, decimal_places=6, null=True)
    postal_code = models.CharField('postal_code', max_length=20)
    country = models.CharField('country', max_length=50)
    pur_system = models.BooleanField('pur_order_sy')
    bill_name = models.CharField('billing_name', max_length=255, unique=True, null=True)
    bill_phone = models.IntegerField('billing_phone', unique=True, null=True)
    bill_email = models.EmailField('company_email', unique=True, null=True)
    auth_prsnl_first_name = models.CharField('auth_personel_frst_name', max_length=100, null=True)
    auth_prsnl_last_name = models.CharField('auth_personel_last_name', max_length=100, null=True)
    auth_prsnl_title = models.CharField('auth_personel_title', max_length=20, choices=TITLE_CHOICES, null=True)
    preferred_mode = models.CharField('preferred_mode', max_length=100, choices=PREFERRED_MODE_CHOICES)
    sub_newsletter = models.BooleanField('sub_newsletter', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        return super(CorporateClient,self).save(*args, **kwargs)

    def get_name(self):
        return self.company_name

    def get_type(self):
        return self.company_type

    def get_email(self):
        return self.main_contact_email

    def get_phone(self):
        return self.main_contact_number

    def get_address(self):
        return self.address

    def get_nature(self):
        return self.nature_of_business

    def get_industry(self):
        return self.industry_sector

    def get_employees(self):
        return self.no_of_employees

    def get_vat(self):
        return self.vat_reg_no

    class Meta:
        db_table = 'corporate_client'
