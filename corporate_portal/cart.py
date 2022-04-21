import random
from booking.models import CCart

CART_ID_SESSION_KEY = 'cor_cart_id'

def _cart_id(request):
    if request.session.get(CART_ID_SESSION_KEY, '')=='':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    cart_id = ''
    characters = 'QWERTYUIOPLKJHGFDSAZXCVBNM0987654321mnbvcxzasdfghjklpoiuytrewq123345678907'
    cart_id_length = 15
    for i in range(cart_id_length):
        cart_id+=characters[random.randint(0, len(characters)-1)]
    return cart_id

def get_cart_item(request):
    return CCart.objects.get(cart_id=_cart_id(request))

def add_to_cart(request, client, appointment, quantity=1):
    """
    This function adds to the cart in the database and stores the cart id in the session
    request:
    client: client object/instance
    appointment: appointment object/instance
    product: product object/instance
    """
    cart = CCart(cart_id=_cart_id(request), client=client, appointment=appointment, quantity=quantity)
    cart.save()
    return cart