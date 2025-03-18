from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Product, Cart, CartItem

def index(request):
    product_list = Product.objects.all()
    context = {'product_list': product_list}
    return render(request, 'kiosk/index.html', context)

def add_to_cart(request):

    if request.method == 'POST':
        request_data = json.load(request)

        # If there is no cart_id set yet we are going to need one, otherwise use whet we were given
        if "cart_id" not in request_data or request_data['cart_id'] == -1:
            cart = Cart()
            cart.save()
        else:
            cart = Cart.objects.get(pk=request_data['cart_id'])

        # Create a cartitem with the product selected
        added_product = Product.objects.get(pk=request_data['product_id'])
        added_product.save()
        cart_item = CartItem(cart_id=cart, product_id=added_product)
        cart_item.save()

    return JsonResponse(get_cart_content(cart.id))


def get_cart_content(cart_id):

    # Get the cart in question and all items in it
    cart = Cart.objects.get(pk=cart_id)
    cart_items = list(CartItem.objects.filter(cart_id=cart))

    # Send back a web consumable objects
    return {
        'id': cart.id,
        'cart_items': [{'name': cart_item.product_id.name,'price': cart_item.product_id.price} for cart_item in cart_items],
        'total_price': sum([cart_item.product_id.price for cart_item in cart_items])
    }

