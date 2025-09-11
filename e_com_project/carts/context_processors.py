from .models import CartItem

def cart_items(request):
    cart_items = CartItem.objects.all()
    total_cart_items = cart_items.count()
    return dict(total_cart_items=total_cart_items)