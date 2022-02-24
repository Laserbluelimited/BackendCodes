from django.test import TestCase
from .models import User, Contact, Phone


def id_increment(model, initial):
    last_value = model.objects.all().order_by('id').last()
    if not last_value:
        new_id = initial
    else:
        new_id = last_value.id + 1
    return new_id


# Create your tests here.
class AuthTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='roli', email='roli@gmail.com', password='roli')
        User.objects.create_user(username='ella', email='ella@gmail.com', password='ella')
        User.objects.create_user(username='sarah', email='sarah@gmail.com', password='sarah')


    def test_user_creation(self):
        user = User.objects.get(username='roli')
        self.assertEqual(user.email, 'roli@gmail.com')

    def test_contact_creation(self):
        user = User.objects.get(username='roli')
        user2 = User.objects.get(email='ella@gmail.com')
        user3 = User.objects.get(email='sarah@gmail.com')
        user_contact = Contact.objects.create(id=id_increment(Contact,111000), user=user, street='Lagos', address_line1='Ijede', address_line2='Bustop', postal_code='1234')
        user_contact2 = Contact.objects.create(id = id_increment(Contact, 1110000), user=user2, street='IKorodu', address_line1='Gbaga', address_line2='Bustop', postal_code='1235')
        user_contact3 = Contact.objects.create(id = id_increment(Contact, 1110000), user=user3, street='Igbogbo', address_line1='Furniture', address_line2='Bustop', postal_code='1235')
        
        print(user_contact3.id)
        self.assertEqual(user_contact.postal_code, '1234')
        self.assertEqual(user_contact2.user.id, user2.id)

    def test_phone_creation(self):
        user = User.objects.get(username='roli')
        user2 = User.objects.get(email='ella@gmail.com')
        user3 = User.objects.get(email='sarah@gmail.com')
        phone1 = Phone.objects.create(id=id_increment(Phone, 1120000), user=user, phone_number='09054583218')
        phone2 = Phone.objects.create(id=id_increment(Phone, 1120000), phone_number='09056786123', user=user)

        self.assertEqual(phone1.user.id, user.id)
        self.assertEqual(phone2.id, 1120001)
