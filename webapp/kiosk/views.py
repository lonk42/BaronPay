from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import json
from .models import Product, Cart, CartItem, Card

def index(request):
    product_list = Product.objects.filter(enabled=True).order_by('ordering_priority')
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
        cart_item = CartItem(cart=cart, product=added_product, price=added_product.price)
        cart_item.save()

        return JsonResponse(get_cart_content(cart.id))

def remove_from_cart(request):

    if request.method == 'POST':
        request_data = json.load(request)

        # Technically its impossible to have an item to remove without a cart id already set
        cart = Cart.objects.get(pk=request_data['cart_id'])

        # Set the item to 'removed'
        cart_item = CartItem.objects.filter(id=request_data['cart_item_id']).first()
        cart_item.removed = True
        cart_item.save()

        return JsonResponse(get_cart_content(cart.id))

def get_cart_content(cart):

    # Get the cart in question along with the card number and all items in it
    cart = Cart.objects.get(pk=cart)
    cart_items = list(CartItem.objects.filter(cart=cart, removed=False))
    if cart.card is None:
        card_number = ''
    else:
        card_number = cart.card.card_number

    # Send back a web consumable objects
    return {
        'id': cart.id,
        'cart_items': [{'id': cart_item.id, 'name': cart_item.product.name,'price': cart_item.price, 'discount_text': cart_item.product.discount_text} for cart_item in cart_items],
        'total_price': sum([cart_item.price for cart_item in cart_items]),
        'card_number': card_number
    }

def card_scanned(request):

    if request.method == 'POST':
        request_data = json.load(request)

        # If there is no cart_id set yet we are going to need one, otherwise use whet we were given
        if "cart_id" not in request_data or request_data['cart_id'] == -1:
            cart = Cart()
            cart.save()
        else:
            cart = Cart.objects.get(pk=request_data['cart_id'])

        # If this is the first time seeing this card number create it
        card = Card.objects.filter(card_number=request_data['card_number']).first()
        if card is None:
            card = Card(card_number=request_data['card_number'])
            card.save()

        # Update the scanned field for this card
        card.last_scanned = timezone.now()
        card.save()

        # Add this card to the cart
        cart.card = card
        cart.save()

        return JsonResponse(get_cart_content(cart.id))

def finish_cart(request):

    if request.method == 'POST':
        request_data = json.load(request)

        cart = Cart.objects.get(pk=request_data['cart_id'])
        cart.completion_status = request_data['completion_status']
        cart.datetime_completed = timezone.now()
        cart.save()

        return JsonResponse({'success': True})
