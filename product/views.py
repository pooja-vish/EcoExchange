from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import Truncator
from user_details.models import  Member
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
    product = get_object_or_404(Product, product_id=product_id)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None

    cart_item, created = CartItem.objects.get_or_create(user=member, id=product_id)
    print(cart_item)
    if product.quantity - cart_item.quantity > 0:
        cart_item.quantity += 1
        cart_item.save()
        success = True
        message = ''
    else:
        success = False
        message = 'Sorry, this product is currently unavailable.'

    if is_ajax:

        subtotal = sum(item.get_total_price() for item in CartItem.objects.filter(user=member))
        total_price = subtotal   # Assuming flat shipping rate of $3

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
    product = get_object_or_404(Product, product_id=item_id)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None

    cart_item, created = CartItem.objects.get_or_create(user=member, id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    if is_ajax:
        subtotal = sum(item.get_total_price() for item in CartItem.objects.filter(user=member))
        total_price = subtotal  # Assuming flat shipping rate of $3
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
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None
    cart_item = get_object_or_404(CartItem, id=item_id, user=member)
    cart_item.delete()

    if is_ajax:
        subtotal = sum(item.get_total_price() for item in CartItem.objects.filter(user=member))
        total_price = subtotal
        return JsonResponse({
            'success': True,
            'subtotal': subtotal,
            'total_price': total_price
        })

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    # Fetch the Member instance using the username of the logged-in user
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None

    if member:
        # Fetch cart items for the member
        cart_items = CartItem.objects.filter(user=member)
        print("Cart items queryset:", cart_items.query)  # Print the SQL query for debugging
        print("Cart items:", list(cart_items))  # Print the cart items

        # Calculate total price
        total_price = sum(item.get_total_price() for item in cart_items if item.is_available)
        print("Total price:", total_price)
    else:
        cart_items = []
        total_price = 0
        print("Member not found for the user")

    return render(request, 'product/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

def homepage(request):
    product_list = Product.objects.all()
    return render(request,template_name='product/homepage.html',context={'product_list':product_list})


def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)
    return render(request,template_name='product/product_detail.html',context={'product':product})


def aboutus (request):
    return render(request,'product/aboutus.html')

