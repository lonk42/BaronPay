from django.contrib import admin

from .models import Product
admin.site.register(Product)

from .models import Card
admin.site.register(Card)