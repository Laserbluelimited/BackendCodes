from django.test import TestCase
from .models import Doctor,Clinic,ClinicLocation
from authentication.models import User, Contact


def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id

# Create your tests here.

class ClinicMgtTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='roli', email='roli@gmail.com', password='roli')
        User.objects.create_user(username='ella', email='ella@gmail.com', password='ella')
        User.objects.create_user(username='hospital', email='hospital@gmail.com', password='hospital')

    def test_clinic_creation(self):
        user1 = User.objects.get(email='hospital@gmail.com')
        user1_contact = Contact.objects.create(id=id_increment(Contact,111000), user=user1, street='Lagos', address_line1='Ijede', address_line2='Bustop', postal_code='1234')
        clinic1 = Clinic.objects.create(id=id_increment(Clinic,1130000), user=user1, name='God\'s Grace hospital', contact=user1_contact)

        self.assertEqual(clinic1.user, user1)
        self.assertEqual(clinic1.user.email, user1.email)
        print(clinic1.contact.user.id)

    def test_doctor_creation(self):
        user1 = User.objects.get(email='hospital@gmail.com')
        user2 = User.objects.get(email='ella@gmail.com')
        user2.first_name = 'Ella'
        user2.last_name = 'Unoke'
        user1_contact = Contact.objects.create(id=id_increment(Contact,111000), user=user1, street='Lagos', address_line1='Ijede', address_line2='Bustop', postal_code='1234')
        clinic1 = Clinic.objects.create(id=id_increment(Clinic,1130000), user=user1, name='God\'s Grace hospital', contact=user1_contact)
        doctor1 = Doctor.objects.create(id=id_increment(Doctor,1140000), user=user2, contact=user1_contact, clinic=clinic1)

        self.assertEqual(doctor1.user, user2)
        self.assertEqual(doctor1.clinic.user.email, clinic1.user.email)

    def test_clinic_verification(self):
        user1 = User.objects.get(email='hospital@gmail.com')
        user1_contact = Contact.objects.create(id=id_increment(Contact,111000), user=user1, street='Lagos', address_line1='Ijede', address_line2='Bustop', postal_code='1234')
        clinic1 = Clinic.objects.create(id=id_increment(Clinic,1130000), user=user1, name='God\'s Grace hospital', contact=user1_contact)
        clinic1.unverify()
        clinic1.make_available()

        self.assertEqual(clinic1.available_to_work, True)
        self.assertEqual(clinic1.verified, False)