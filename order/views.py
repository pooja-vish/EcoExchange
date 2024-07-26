# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from product.models import Product
from user_details.models import Member
from django.utils import timezone


@login_required
@permission_required('order.view_order', raise_exception=True)
def user_orders(request):
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None
    orders = Order.objects.filter(user_id=member)
    order_items = OrderItem.objects.filter(order_id__in=orders)
    context = {'orders': orders, 'order_items': order_items}
    return render(request, 'order/user_orders.html', context)

@login_required
@permission_required('order.view_order', raise_exception=True)
def seller_products(request):
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None

    products = Product.objects.filter(user=member)
    order_items1 = OrderItem.objects.filter(product_id__in=products)
    orders1 = Order.objects.filter(order_id__in=[item.order_id.order_id for item in order_items1])
    users = {order.user_id for order in orders1}
    context = {'products': products, 'order_items1': order_items1, 'orders1': orders1, 'users': users}
    return render(request, 'order/seller_products.html', context)


@login_required
@permission_required('order.change_order', raise_exception=True)
def update_order_status(request, order_id):
    print("hello")
    if request.method == "POST":
        order = get_object_or_404(Order, pk=order_id)
        order_status = request.POST.get("order_status")
        order.order_status = order_status
        order.save()
    return redirect(request.META.get('HTTP_REFERER', 'user_orders'))
