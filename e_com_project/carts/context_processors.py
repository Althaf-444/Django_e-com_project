from .models import CartItem ,Cart
from .views import _cart_id
def cart_items(request):
    total_cart_items = 0
    if "admin" in request.path :
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart = cart[:1])
            for cart_item in cart_items:
                total_cart_items += cart_item.quantity
        except Cart.DoesNotExist:
            total_cart_items = 0
    
    return dict(total_cart_items=total_cart_items)