from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.4)
    thumbnail_file = models.CharField(max_length=2048)

    def __str__(self):
        return self.name

class Card(models.Model):
    card_number = models.CharField(max_length=12)
    alias = models.CharField(max_length=64, default='')
    datetime_created = models.DateTimeField("date created", auto_now_add=True, blank=True)
    last_scanned = models.DateTimeField("date completed", blank=True, null=True)

    def __str__(self):
        return ("id: %s, card_number: %s, datetime_created: %s, last_scanned: %s") % (self.id, self.card_number, self.datetime_created, self.last_scanned)

class Cart(models.Model):
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True)
    datetime_created = models.DateTimeField("date created", auto_now_add=True, blank=True)
    datetime_completed = models.DateTimeField("date completed", blank=True, null=True)
    completion_status = models.CharField(max_length=64, default='')

    def __str__(self):
        return ("id: %s, card_id: %s, datetime_created: %s, datetime_completed: %s, completion_status: %s") % (self.id, self.card_id.id, self.datetime_created, self.datetime_completed, self.completion_status)

class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField("date created", auto_now_add=True, blank=True)

    def __str__(self):
        return ("id: %s, product_id: %s, datetime_created: %s") % (self.id, self.product_id, self.datetime_created)
