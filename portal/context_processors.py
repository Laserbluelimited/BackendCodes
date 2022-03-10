from clinic_mgt.models import Clinic, Doctor
from prod_mgt.models import Product

def portal_context(request):
    clinics = Clinic.objects.all()
    products = Product.objects.all()
    doctors = Doctor.objects.all()
    return {'clinics':clinics, 'products':products, 'doctors':doctors}
