from django.contrib import admin

from .models import Product, Card, Cart, CartItem
admin.site.register(Product)
admin.site.register(Card)
admin.site.register(Cart)
admin.site.register(CartItem)