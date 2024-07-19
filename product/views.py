from django.shortcuts import render, get_object_or_404
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
def add_item_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if product.quantity > 0:
        cart_item.quantity += 1
        cart_item.save()
        success = True
        message = ''
    else:
        success = False
        message = 'Sorry, this product is currently unavailable.'

    if request.is_ajax():
        subtotal = sum(item.get_total_price() for item in CartItem.objects.filter(user=request.user))
        total_price = subtotal + 3  # Assuming flat shipping rate of $3
        return JsonResponse({
            'success': success,
            'message': message,
            'quantity': cart_item.quantity,
            'total': cart_item.get_total_price(),
            'subtotal': subtotal,
            'total_price': total_price
        })

    return redirect('cart_detail')

@login_required
def remove_item_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    if request.is_ajax():
        subtotal = sum(item.get_total_price() for item in CartItem.objects.filter(user=request.user))
        total_price = subtotal + 3  # Assuming flat shipping rate of $3
        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity if cart_item.id else 0,
            'total': cart_item.get_total_price() if cart_item.id else 0,
            'subtotal': subtotal,
            'total_price': total_price
        })

    return redirect('cart_detail')

@login_required
def delete_item_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()

    if request.is_ajax():
        subtotal = sum(item.get_total_price() for item in CartItem.objects.filter(user=request.user))
        total_price = subtotal + 3  # Assuming flat shipping rate of $3
        return JsonResponse({
            'success': True,
            'subtotal': subtotal,
            'total_price': total_price
        })

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items if item.is_available)
    return render(request, 'product/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

def homepage(request):
    product_list = Product.objects.all()
    return render(request,template_name='product/homepage.html',context={'product_list':product_list})


def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)
    return render(request,template_name='product/product_detail.html',context={'product':product})

