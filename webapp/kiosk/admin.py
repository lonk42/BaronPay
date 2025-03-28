from django.contrib import admin
from .models import Product, Card, Cart, CartItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'enabled', 'notes', 'discount_text', 'thumbnail_file', 'ordering_priority')
admin.site.register(Product, ProductAdmin)

class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'card_number', 'alias', 'datetime_created', 'last_scanned')
admin.site.register(Card, CardAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime_created', 'datetime_completed', 'completion_status', 'items')
    def items(self, obj):
        return [item.product_id.name for item in list(CartItem.objects.filter(cart_id=obj, removed=False))]
admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'price', 'removed', 'datetime_created')
    def cart(self, obj):
        return obj.cart_id.id
    def product(self, obj):
        return obj.product_id.name
    def price(self, obj):
        return obj.product_id.price
admin.site.register(CartItem, CartItemAdmin)