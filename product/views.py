from django.shortcuts import render, get_object_or_404
from django.utils.text import Truncator

from product.models import Product


# Create your views here.


def products_list(request):
    product_list = Product.objects.all()
    for product in product_list:
        product.short_description = Truncator(product.product_description).chars(100)
    return render(request,template_name='product/product_list.html',context={'product_list':product_list})

def products_detail(request,product_id):
    product = get_object_or_404(Product,id=product_id))
    return render(request,template_name='product/product_detail.html',context={'product':product})
