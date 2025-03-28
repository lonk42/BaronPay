from django.db import models
from datetime import datetime
import time

def nice_time_format(datetime):
    if datetime is None:
        return "None"

    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return (datetime + offset).strftime("%Y-%m-%d %H:%M:%S")

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.4)
    enabled = models.BooleanField(default=True)
    notes = models.CharField(max_length=1024, default="", blank=True)
    discount_text = models.CharField(max_length=100, default="", blank=True)
    thumbnail_file = models.CharField(max_length=2048)
    ordering_priority = models.IntegerField(default=50, blank=True)

    def __str__(self):
        enabled_text = "" if self.enabled else "[Disabled] "
        discount_text = "" if self.discount_text == "" else ", Discounted '%s'" % self.discount_text
        notes = "" if self.notes == "" else ", '%s'" % self.notes
        return ("%s%s, $%s, thumbnail: %s, order: %d%s%s") % (enabled_text, self.name, self.price, self.thumbnail_file, self.ordering_priority, notes, discount_text)

class Card(models.Model):
    card_number = models.CharField(max_length=12)
    alias = models.CharField(max_length=64, default='')
    datetime_created = models.DateTimeField("date created", auto_now_add=True, blank=True)
    last_scanned = models.DateTimeField("date completed", blank=True, null=True)

    def __str__(self):
        alias_text = "" if self.alias == "" else " '%s'" % (self.alias)
        return ("(%s) %s%s, created: %s, last_scanned: %s") % (self.id, self.card_number, alias_text, nice_time_format(self.datetime_created), nice_time_format(self.last_scanned))

class Cart(models.Model):
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True)
    datetime_created = models.DateTimeField("date created", auto_now_add=True, blank=True)
    datetime_completed = models.DateTimeField("date completed", blank=True, null=True)
    completion_status = models.CharField(max_length=64, default='')

    def __str__(self):

        completed_text = "Completed " if self.completion_status == "complete" else "[%s] " % (self.completion_status)

        # The cart_id can be None, need to lint this
        card_number = "[No Card]" if self.card_id is None else self.card_id.card_number

        # Get a list of items assocaited with this cart
        cart_items = [item.product_id.name for item in list(CartItem.objects.filter(cart_id=self, removed=False))]
        
        return ("(%s) %s, created: %s, %s%s, status: %s, Items: %s") % (self.id, card_number, completed_text, nice_time_format(self.datetime_completed), nice_time_format(self.datetime_created), self.completion_status, cart_items)

class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    removed = models.BooleanField(default=False)
    datetime_created = models.DateTimeField("date created", auto_now_add=True, blank=True)

    def __str__(self):
        removed_text = "" if not self.removed else ", [REMOVED]"
        return ("(%s)%s, added: %s%s") % (self.id, self.product_id.name, nice_time_format(self.datetime_created), removed_text)
