import random
from .models import Cart

CART_ID_SESSION_KEY = 'cart_id'

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
    return Cart.objects.get(cart_id=_cart_id(request))

def add_to_cart(request, client, appointment, product, quantity=1):
    """
    This function adds to the cart in the database and stores the cart id in the session
    request:
    client: client object/instance
    appointment: appointment object/instance
    product: product object/instance
    """
    cart = Cart(cart_id=_cart_id(request), client=client, appointment=appointment, product=product)
    cart.save()
    return cart

def delete_cart(request):
    if 'cart_id' in request.session:
        cart = Cart.objects.get(cart_id=request.session['cart_id'])
        cart.appointment.update_status(0)
        cart.appointment.time_slot.update_status(0)
        cart.save()
        del request.session['cart_id']
        request.session.modified=True
