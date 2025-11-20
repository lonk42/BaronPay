from django.contrib import admin
from django.urls import reverse, path
from django.utils.html import format_html
from django.shortcuts import render
from django.db.models import Sum, Count
from collections import defaultdict
from datetime import datetime
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

# Custom Admin Views
class KioskAdminSite(admin.AdminSite):
    site_header = 'BaronPay Administration'
    site_title = 'BaronPay Admin'
    index_title = 'BaronPay Admin'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('daily-sales/', self.admin_view(self.daily_sales_view), name='daily_sales'),
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_daily_sales_link'] = True
        return super().index(request, extra_context)

    def daily_sales_view(self, request):
        # Get all completed carts with their items
        completed_carts = Cart.objects.filter(completion_status='complete').exclude(datetime_completed=None)

        # Group sales by date
        daily_sales = defaultdict(lambda: {'products': defaultdict(lambda: {'count': 0, 'revenue': 0}), 'total': 0})

        for cart in completed_carts:
            # Get the date of completion (without time)
            completion_date = cart.datetime_completed.date()

            # Get all cart items that weren't removed
            cart_items = CartItem.objects.filter(cart=cart, removed=False)

            for item in cart_items:
                product_name = item.product.name
                price = float(item.price)

                daily_sales[completion_date]['products'][product_name]['count'] += 1
                daily_sales[completion_date]['products'][product_name]['revenue'] += price
                daily_sales[completion_date]['total'] += price

        # Convert to sorted list for template (most recent first)
        sales_data = []
        for date in sorted(daily_sales.keys(), reverse=True):
            products = []
            for product_name, data in sorted(daily_sales[date]['products'].items()):
                products.append({
                    'name': product_name,
                    'count': data['count'],
                    'revenue': data['revenue']
                })

            sales_data.append({
                'date': date,
                'products': products,
                'total': daily_sales[date]['total']
            })

        context = {
            **self.each_context(request),
            'title': 'Daily Sales Summary',
            'sales_data': sales_data,
        }

        return render(request, 'admin/kiosk/daily_sales.html', context)

# Register the custom admin site
admin_site = KioskAdminSite(name='kioskadmin')
admin_site.register(Product, ProductAdmin)
admin_site.register(Card, CardAdmin)
admin_site.register(Cart, CartAdmin)
admin_site.register(CartItem, CartItemAdmin)