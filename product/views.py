from django.shortcuts import render
from django.utils.text import Truncator

from product.models import Product, CartItem
from django.contrib.auth.decorators import login_required


# Create your views here.


def products_list(request):
    product_list = Product.objects.all()
    for product in product_list:
        product.short_description = Truncator(product.product_description).chars(100)
    return render(request,template_name='product/product_list.html',context={'product_list':product_list})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if product.quantity > 0:
        cart_item.is_available = True
        if created:
            cart_item.quantity = 1  # Set initial quantity to 1
        else:
            if product.quantity > cart_item.quantity:
                cart_item.quantity += 1  # Increment quantity if there's enough stock
            else:
                messages.error(request, 'Sorry, not enough quantity available for this product.')
                return redirect('cart_detail')
    else:
        cart_item.is_available = False
        messages.error(request, 'Sorry, this product is currently unavailable.')

    cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items if item.is_available)
    return render(request, 'product/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

def homepage(request):
    product_list = Product.objects.all()
    return render(request,template_name='product/homepage.html',context={'product_list':product_list})

