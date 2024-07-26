from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import Truncator
from user_details.models import Member
from product.models import Product, CartItem, Auction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from django.views import View
from .forms import AuctionForm
from django.views.generic import ListView
# adding these
from django.contrib import messages
from coins.models import Coins
from order.models import Order, OrderItem
from django.db import transaction

class AuctionCreateView(View):
    def get(self, request):
        form = AuctionForm()
        return render(request, 'product/auction_form.html', {'form': form})

    def post(self, request):
        form = AuctionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})


class AuctionUpdateView(View):
    def get(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        form = AuctionForm(instance=auction)
        return render(request, 'product/auction_form.html', {'form': form})

    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        form = AuctionForm(request.POST, instance=auction)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})


class AuctionDeleteView(View):
    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        auction.delete()
        return JsonResponse({'success': True})


class AuctionListView(ListView):
    model = Auction
    template_name = 'product/auction_list.html'

    def get_queryset(self):
        try:
            member = Member.objects.get(username=self.request.user.username)
        except Member.DoesNotExist:
            member = None
        return Auction.objects.filter(product__user=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auctions'] = self.get_queryset()
        return context


def products_list(request):
    product_list = Product.objects.all()
    for product in product_list:
        product.short_description = Truncator(product.product_description).chars(100)
    return render(request, template_name='product/product_list.html', context={'product_list': product_list})


@login_required
def add_to_cart(request, product_id):
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product = get_object_or_404(Product, product_id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        cart_item, created = CartItem.objects.get_or_create(user=member, product=product)
        if not created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({'message': 'Item added to the cart.'})
    return JsonResponse({'message': 'Failed to add item to the cart.'}, status=400)


def addtocart(request, product_id):
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None

    product = get_object_or_404(Product, product_id=product_id)

    cart_item, created = CartItem.objects.get_or_create(user=member, product=product)
    if not created:
        cart_item.product = product
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()

    return redirect('cart_detail')


@login_required
def add_item_to_cart(request, product_id):

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None

    cart_item, created = CartItem.objects.get_or_create(user=member, id=product_id)
    print(cart_item)
    product = cart_item.product

    if product.quantity - cart_item.quantity > 0:
        cart_item.quantity += 1
        cart_item.save()
        success = True
        message = ''
    else:
        cart_item.save()
        success = False
        message = 'Sorry, this product is currently unavailable.'

    if is_ajax:

        subtotal = sum(item.get_total_price() for item in CartItem.objects.filter(user=member))
        total_price = subtotal
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
    print("hello")
    print("hi")

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None

    cart_item, created = CartItem.objects.get_or_create(user=member, id=item_id)
    print(cart_item)
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

    return render(
        request,
        'product/cart_detail.html',
        {'cart_items': cart_items, 'total_price': total_price}
    )


def homepage(request):
    product_list = Product.objects.all()
    return render(request, template_name='product/homepage.html', context={'product_list': product_list})


def product_detail(request, pk):
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None
    product = get_object_or_404(Product, pk=pk)
    cart_item = CartItem.objects.filter(user=member, product=product).first()
    cart_quantity = cart_item.quantity if cart_item else 0

    return render(
        request,
        template_name='product/product_detail.html',
        context={'product': product, 'cart_quantity': cart_quantity}
    )


def aboutus(request):
    return render(request, 'product/aboutus.html')


def auction_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    auction = get_object_or_404(Auction, product=product)
    return render(request, 'product/auction.html', {'product': product, 'auction': auction})


def checkout(request):
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None

    cart_items = CartItem.objects.filter(user=member)
    item_totals = [(item, item.product.price * item.quantity) for item in cart_items]
    total_cost = sum(total for item, total in item_totals)
    success_message = None

    if request.method == 'POST':
        if member.coin_balance >= total_cost:
            with transaction.atomic():
                for item in cart_items:
                    item.product.quantity -= item.quantity
                    item.product.save()
                    item.delete()
                member.coin_balance -= total_cost
                member.save()

                # Create order
                order_now=Order.objects.create(
                    user_id = member,
                    # order_date = timezone.now
                    order_amount = total_cost,
                )
                for item in cart_items:
                    OrderItem.objects.create(
                        order_id=order_now,
                        product_id = item.product,
                        quantity = item.quantity
                    )


    #        # success_message = "Order placed successfully!"
    #         messages.success(request, 'Order placed successfully!')
    #         return redirect('checkout')
    #
    # return render(request, 'product/checkout.html', {
    #     'cart_items': item_totals,
    #     'total_cost': total_cost,
    #     'success_message': success_message,
    #     'error_message': 'Insufficient coins to complete the purchase.' if request.method == 'POST' and member.coin_balance < total_cost else None
    # })
            messages.success(request, 'Order placed successfully!')
            return redirect('checkout')

        else:
            messages.error(request, 'Insufficient coins to complete the purchase.')

    return render(request, 'product/checkout.html', {
            'cart_items': item_totals,
            'total_cost': total_cost,
    })