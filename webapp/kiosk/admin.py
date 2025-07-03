from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Product, Card, Cart, CartItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'enabled', 'notes', 'discount_text', 'thumbnail_file', 'ordering_priority')
admin.site.register(Product, ProductAdmin)

class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'card_number', 'alias', 'alias_required', 'datetime_created', 'last_scanned')
admin.site.register(Card, CardAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'card_number', 'datetime_created', 'datetime_completed', 'sold', 'completion_status', 'total', 'items')
    def items(self, obj):
        return [item.product.name for item in list(CartItem.objects.filter(cart=obj, removed=False))]
    def total(self, obj):
        return "$%s" % (sum([cart_item.price for cart_item in list(CartItem.objects.filter(cart=obj, removed=False))]))
    def sold(self, obj):
        if obj.completion_status == 'complete':
            return True
        return False
    sold.boolean = True
    def card_number(self, obj):
        if obj.card is not None:
            link = reverse("admin:kiosk_card_change", args=[obj.card.id])
            return format_html('<a href="{}">{}</a>', link, obj.card.card_number)
        return "[No Card]"
admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart_id', 'product_name', 'price', 'retained', 'sold', 'datetime_created')
    def cart_id(self, obj):
        link = reverse("admin:kiosk_cart_change", args=[obj.cart.id])
        return format_html('<a href="{}">{}</a>', link, obj.cart.id)
    def product_name(self, obj):
        link = reverse("admin:kiosk_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', link, obj.product.name)
    def retained(self, obj):
        return not obj.removed
    retained.boolean = True
    def sold(self, obj):
        if obj.cart.completion_status == 'complete':
            return True
        return False
    sold.boolean = True
admin.site.register(CartItem, CartItemAdmin)