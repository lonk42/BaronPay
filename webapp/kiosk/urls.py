from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart", views.remove_from_cart, name="remove_from_cart"),
    path("card_scanned", views.card_scanned, name="card_scanned"),
    path("submit_card_prompt", views.submit_card_prompt, name="submit_card_prompt"),
    path("finish_cart", views.finish_cart, name="finish_cart"),
]