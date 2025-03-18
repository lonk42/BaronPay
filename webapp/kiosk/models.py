from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.4)
    thumbnail_file = models.CharField(max_length=2048)

    def __str__(self):
        return self.name

class User(models.Model):
    card_id = models.CharField(max_length=12)
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField("date created", auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    datetime_created = models.DateTimeField("date created", auto_now_add=True, blank=True)
    datetime_completed = models.DateTimeField("date completed", blank=True, null=True)

    def __str__(self):
        return ("id: %s, user_id: %s, datetime_created: %s, datetime_completed: %s") % (self.id, self.user_id, self.datetime_created, self.datetime_completed)

class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField("date created", auto_now_add=True, blank=True)

    def __str__(self):
        return ("id: %s, product_id: %s, datetime_created: %s") % (self.id, self.product_id, self.datetime_created)
