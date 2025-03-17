from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Product

def index(request):
    product_list = Product.objects.all()
    context = {'product_list': product_list}
    return render(request, 'kiosk/index.html', context)

def add_to_cart(request):
    if request.method == 'POST':
         data = json.load(request)
    return JsonResponse({'returned': data})