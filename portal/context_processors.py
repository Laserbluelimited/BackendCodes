from clinic_mgt.models import Clinic
from prod_mgt.models import Product

def portal_context(request):
    clinics = Clinic.objects.all()
    products = Product.objects.all()
    return {'clinics':clinics, 'products':products}
