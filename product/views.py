from django.shortcuts import render
from django.utils.text import Truncator

from product.models import Product


# Create your views here.

def products_list(request):
    product_list = Product.objects.all()
    for product in product_list:
        product.short_description = Truncator(product.product_description).chars(100)
    return render(request,template_name='product/product_list.html',context={'product_list':product_list})