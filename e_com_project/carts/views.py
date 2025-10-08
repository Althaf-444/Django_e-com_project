from django.shortcuts import render , redirect ,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product , Variation
from .models import Cart , CartItem
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
def cart(request , total = 0 ,quantity = 0 , cart_items = None):

    cart_items = []
    tax = 0
    grand_total = 0

    try:
        if request.user.is_authenticated:
              cart_items = CartItem.objects.filter(user = request.user , is_active = True)
        else:
            cart        = Cart.objects.get(cart_id = _cart_id(request))
            cart_items  = CartItem.objects.filter(cart = cart , is_active = True)

        for cart_item in cart_items:
            total    += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist :
        pass

    context = {
        'total'      : total,
        'quantity'   : quantity,
        'cart_items' : cart_items,
        'tax'        :tax ,
        'grand_total': grand_total,
    }

    return render(request , 'store/cart.html' , context)

def _cart_id(request):

    cart = request.session.session_key

    if not cart:
        cart = request.session.create()

    return cart


def add_cart(request , product_id):
    product = Product.objects.get(id = product_id)
    current_user = request.user

    if current_user.is_authenticated:
        product_variations = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product= product ,variation_category__iexact = key , variation_value__iexact = value)
                    product_variations.append(variation)

                except:
                    pass

    # ===================--------- cart items ----------=======================================================

        is_cart_item = CartItem.objects.filter(product = product , user = current_user).exists()

        if is_cart_item:

            cart_items = CartItem.objects.filter(product = product , user = current_user)
            ex_cart_item = []
            id = []
            for item in cart_items :
                    exists_cart_item = item.variations.all()
                    ex_cart_item.append(list(exists_cart_item))
                    id.append(item.id) # type: ignore

            if  product_variations in ex_cart_item :
                index = ex_cart_item.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product = product , id = item_id )
                item.quantity += 1
                item.save()

            else :
                if len(product_variations) > 0 :
                        item = CartItem.objects.create( product = product , user = current_user, quantity = 1,)
                        item.variations.clear()
                        item.variations.add(*product_variations)
                item.save()

        else :
            cart_items = CartItem.objects.create(
                    product = product ,
                     user = current_user,
                    quantity = 1,
                )
            if len(product_variations) > 0 :
                    cart_items.variations.clear()
                    cart_items.variations.add(*product_variations)
            cart_items.save()
        return redirect('cart')





    else:

        product_variations = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product= product ,variation_category__iexact = key , variation_value__iexact = value)
                    product_variations.append(variation)

                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request),
            )
        cart.save()

    # ===================--------- cart items ----------=======================================================

        is_cart_item = CartItem.objects.filter(product = product , cart = cart).exists()

        if is_cart_item:

            cart_items = CartItem.objects.filter(product = product , cart = cart)
            ex_cart_item = []
            id = []
            for item in cart_items :
                    exists_cart_item = item.variations.all()
                    ex_cart_item.append(list(exists_cart_item))
                    id.append(item.id)  # type: ignore

            if  product_variations in ex_cart_item :
                index = ex_cart_item.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product = product , id = item_id )
                item.quantity += 1
                item.save()

            else :
                if len(product_variations) > 0 :
                        item = CartItem.objects.create( product = product ,cart = cart, quantity = 1,)
                        item.variations.clear()
                        item.variations.add(*product_variations)
                item.save()

        else :
            cart_items = CartItem.objects.create(
                    product = product ,
                    cart = cart,
                    quantity = 1,
                )
            if len(product_variations) > 0 :
                    cart_items.variations.clear()
                    cart_items.variations.add(*product_variations)
            cart_items.save()
        return redirect('cart')

def remove_cart(request , product_id , cart_item_id ):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product , id = product_id)

    try:
        cart_item = CartItem.objects.get(cart=cart , product = product , id = cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')

def delete_cart_item(request , product_id ,  cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product , id = product_id)
    cart_item = CartItem.objects.get(cart=cart , product = product , id = cart_item_id)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def checkout(request , total = 0 ,quantity = 0 , cart_items = None):

    cart_items = []
    tax = 0
    grand_total = 0

    try:

        cart        = Cart.objects.get(cart_id = _cart_id(request))
        cart_items  = CartItem.objects.filter(cart = cart , is_active = True)

        for cart_item in cart_items:
            total    += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist :
        pass

    context = {
        'total'      : total,
        'quantity'   : quantity,
        'cart_items' : cart_items,
        'tax'        :tax ,
        'grand_total': grand_total,
    }
    return render(request , 'store/checkout.html',context)