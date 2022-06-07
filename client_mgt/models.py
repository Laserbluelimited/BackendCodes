from statistics import mode
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id




TITLE_CHOICES = (
    ('Miss', 'Miss'),
    ('Mr', 'Mr.'),
    ('Mrs', 'Mrs.'),
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
    ('Sole Trader', 'Sole Trader'),
    ('Limited Company', 'Limited Company'),
    ('Partnership', 'Partnership'),
    ('LLP', 'LLP')
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
    first_name = models.CharField('first_name', max_length=100)
    last_name = models.CharField('last_name', max_length=100)
    email = models.EmailField('email', unique=True)
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, null=True)
    title = models.CharField('title', max_length=20, choices=TITLE_CHOICES, null=True)
    phone = models.CharField('phone_number', unique=False, max_length=15)
    dob = models.DateField('date_of_birth', null=True)
    gender = models.CharField('gender', choices=GENDER_CHOICES, max_length=50, null=True)
    address = models.CharField('address', max_length=255, null=True)
    city = models.CharField('city', max_length=100, null=True)
    long = models.DecimalField('longitude', max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField('latitude', max_digits=9, decimal_places=6, null=True)
    postal_code = models.CharField('postal_code', max_length=20, null=True)
    country = models.CharField('country', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, help_text='Unique Value for product page URL, created from name.')
    status = models.CharField('status', max_length=20, choices=[(0,'visitor'),(1, 'unverified customer'), (2, 'verified customer')], default=0)
    cor_comp = models.ForeignKey('CorporateClient', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'internet_client'

    def __str__(self):
        return self.first_name +' '+ self.last_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = id_increment(InternetClient, 112000)
        if not self.slug:
            name = self.first_name + str(self.id)
            self.slug = slugify(name)
        return super(InternetClient,self).save(*args, **kwargs)

    def update_status(self, status):
        self.status=status
        self.save()

    def get_name(self):
        return self.first_name + " "+ self.last_name

    def get_email(self):
        return self.email

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
    company_name = models.CharField('company name', unique=True, max_length=255)
    slug = models.SlugField(max_length=255, help_text='Unique Value for product page URL, created from name.')
    company_type = models.CharField('company_type', max_length=50, choices=COMPANY_TYPE_CHOICES)
    nature_of_business = models.CharField('nature of business', max_length=255, null=True)
    industry_sector = models.CharField('industry sector', max_length=100)
    vat_reg_no = models.CharField('VAT registartion no', max_length=255)
    main_contact_name = models.CharField('Primary Contact Name', max_length=100)
    main_contact_number = models.CharField('Primary Contact Number', max_length=20, unique=True)
    main_contact_email = models.EmailField('Primary Email', unique=True)
    no_of_employees = models.IntegerField('Number of Employees')
    no_of_years = models.IntegerField('No of years of trade')
    address = models.CharField('address', max_length=255)
    city = models.CharField('city', max_length=100)
    long = models.DecimalField('longitude', max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField('latitude', max_digits=9, decimal_places=6, null=True)
    postal_code = models.CharField('postal_code', max_length=20)
    country = models.CharField('country', max_length=50)
    medium_of_marketing = models.CharField('medium_of_marketing', max_length=1000, null=True)
    avg_no_order = models.IntegerField('avg_no_order', null=True)
    pur_system = models.BooleanField('POS')
    bill_name = models.CharField('Account name', max_length=255, null=True)
    bill_phone = models.CharField('Account contact phone', null=True, max_length=15)
    bill_email = models.EmailField('Account email', null=True)
    auth_prsnl_name = models.CharField('Authorised Personnel Name', max_length=100, null=True)
    # preferred_mode = models.CharField('preferred_mode', max_length=100, choices=PREFERRED_MODE_CHOICES)
    sub_newsletter = models.BooleanField('Newsletter Subscription', default=True)
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

    def get_bill_name(self):
        return self.bill_name

    def get_bill_email(self):
        return self.bill_email

    def get_bill_phone(self):
        return self.bill_phone

    def get_pos(self):
        return self.pur_system

    def get_type(self):
        return self.company_type

    def get_email(self):
        return self.main_contact_email

    def get_phone(self):
        return self.main_contact_number

    def get_address(self):
        return self.address

    def get_city(self):
        return self.city
    
    def get_postal_code(self):
        return self.postal_code

    def get_nature(self):
        return self.nature_of_business

    def get_industry(self):
        return self.industry_sector

    def get_employees(self):
        return self.no_of_employees

    def get_vat(self):
        return self.vat_reg_no

    def get_apn(self):
        return self.auth_prsnl_name


    class Meta:
        db_table = 'corporate_client'
