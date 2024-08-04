import random
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import Truncator
from user_details.models import Member, Transaction
from product.models import Product, CartItem, Auction, Queries

from .forms import AuctionForm, EditProfileForm, QueryForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, TemplateView


from django.views import View
from django.contrib import messages
from coins.models import Coins
from order.models import Order, OrderItem
from django.db import transaction


class AuctionCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        form = AuctionForm(user=request.user)  # Pass the user to the form
        auctions = Auction.objects.filter(product__user=request.user)  # Filter auctions based on the logged-in user
        return render(request, 'product/auction_form.html', {'form': form, 'auctions': auctions})

    def post(self, request):
        form = AuctionForm(request.POST, user=request.user)  # Pass the user to the form
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        auctions = Auction.objects.filter(product__user=request.user)  # Filter auctions based on the logged-in user
        return JsonResponse({'success': False, 'errors': form.errors, 'auctions': auctions})


class AuctionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        form = AuctionForm(instance=auction, user=request.user)  # Pass the user to the form
        auctions = Auction.objects.filter(product__user=request.user)  # Filter auctions based on the logged-in user
        return render(request, 'product/auction_form.html', {'form': form, 'auctions': auctions})

    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        form = AuctionForm(request.POST, instance=auction, user=request.user)  # Pass the user to the form
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        auctions = Auction.objects.filter(product__user=request.user)  # Filter auctions based on the logged-in user
        return JsonResponse({'success': False, 'errors': form.errors, 'auctions': auctions})


class AuctionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, View):

    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        auction.delete()
        return JsonResponse({'success': True})


class AuctionAllListView(LoginRequiredMixin, ListView):
    model = Auction
    template_name = 'product/all_auctions.html'
    context_object_name = 'all_auctions'

    def get_queryset(self):
        user = self.request.user
        return Auction.objects.exclude(product__user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auctions'] = self.get_queryset()
        return context


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


class AuctionRealTimeView(TemplateView):
    template_name = 'product/realtime_bids.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        auction = get_object_or_404(Auction, product=product)
        context['product'] = product
        context['auction'] = auction
        return context


@login_required
def dashboard(request):
    details = Member.objects.filter(username=request.user.username)
    return render(request, 'product/dashboard.html', {'details': details})


def products(request):
    products = []
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'name':
        sort_by = 'product_name'
    if sort_by == 'byprice':
        sort_by = 'price'
    if sort_by == 'pricedesc':
        sort_by = '-price'
    if sort_by:
        product_list = Product.objects.all().order_by(sort_by)

    input_range = request.GET.get('rangeInput')
    if input_range:
        product_list = Product.objects.filter(price__lte=input_range)

    search = request.GET.get('find')
    if search:
        product_list = Product.objects.filter(product_description__icontains=search)

    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')
        print(selected_categories)
        if selected_categories:
            product_list = Product.objects.filter(category__in=selected_categories)

    total_products = Product.objects.all().values('category').distinct()
    print(total_products)
    for product in product_list:
        product.short_description = Truncator(product.product_description).chars(120)
    return render(request, template_name='product/product_list.html',
                  context={'product_list': product_list, 'total_products': total_products})


@login_required
@permission_required('product.add_cartitem', raise_exception=True)
def add_to_cart(request, product_id):
    print("hi")
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product = get_object_or_404(Product, product_id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        cart_item, created = CartItem.objects.get_or_create(user=member, product=product)
        if product.quantity - cart_item.quantity > 0:
            cart_item.quantity  = quantity
            cart_item.save()
            success = True
            message = 'Item has been added to cart'
        else:
            cart_item.save()
            success = False
            message = f'Sorry, only {product.quantity} of this product are currently in stock.'



        return JsonResponse({'message': message })
    return JsonResponse({'message': 'Failed to add item to the cart.'}, status=400)


@login_required
@permission_required('product.add_cartitem', raise_exception=True)
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
@permission_required('product.add_cartitem', raise_exception=True)
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
@permission_required('product.delete_cartitem', raise_exception=True)
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
@permission_required('product.delete_cartitem', raise_exception=True)
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
@permission_required('product.view_cartitem', raise_exception=True)
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


    visited_products = request.COOKIES.get('visited_products', '')
    visited_products_list = visited_products.split(',') if visited_products else []
    visited_product_objects = Product.objects.filter(product_id__in=visited_products_list)

    return render(
        request,
        'product/cart_detail.html',
        {
            'cart_items': cart_items,
            'total_price': total_price,
            'visited_products': visited_product_objects
        }
    )

def homepage(request):
    distinct_categories = Product.objects.values_list('category', flat=True).distinct()
    return render(request, template_name='product/homepage.html', context={'categories_list': distinct_categories})


@login_required
@permission_required('product.view_product', raise_exception=True)
def product_detail(request, pk):
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None

    product = get_object_or_404(Product, pk=pk)
    cart_item = CartItem.objects.filter(user=member, product=product).first()
    cart_quantity = cart_item.quantity if cart_item else 0


    visited_products = request.COOKIES.get('visited_products', '')
    visited_products_list = visited_products.split(',') if visited_products else []

    if str(pk) not in visited_products_list:
        # Ensure the list contains at most 5 items
        if len(visited_products_list) >= 5:
            visited_products_list.pop(0)


        visited_products_list.append(str(pk))


    new_visited_products = ','.join(visited_products_list)

    response = render(
        request,
        template_name='product/product_detail.html',
        context={'product': product, 'cart_quantity': cart_quantity}
    )

    response.set_cookie('visited_products', new_visited_products)

    return response


def aboutus(request):
    return render(request, 'product/aboutus.html')

@login_required
@permission_required('product.view_auction', raise_exception=True)
def auction_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    auction = get_object_or_404(Auction, product=product)
    return render(request, 'product/auction_view.html', {'product': product, 'auction': auction})
@login_required
def support(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            choices = form.cleaned_data['choices']
            description = form.cleaned_data['description']
            member = Member.objects.get(username=request.user)
            ticket_id = random.randint(1000000000, 9999999999)
            while(Queries.objects.filter(ticket_id=ticket_id).exists()):
                ticket_id = random.randint(1000000000, 9999999999)
            query_object = Queries(choices=choices, description=description, user=member, ticket_id=ticket_id)
            query_object.save()
        return redirect('homepage')
    else:
        form = QueryForm()
    return render(request, 'product/support.html', {'form': form})

@login_required
def dashboard(request, section):
    if section == 'home':
        details = Member.objects.get(username=request.user.username)
        return render(request, 'product/dashboard.html', {'details': details})
    elif section == 'edit':
        details = Member.objects.get(username=request.user.username)
        return render(request, 'product/editprofile.html', {'details': details})
    elif section == 'edit_profile':
        if request.method == 'POST':
            user_profile = Member.objects.get(username=request.user)
            form = EditProfileForm(request.POST, instance=user_profile)
            if form.is_valid():
                name = request.POST.get('first_name')
                lastname = request.POST.get('last_name')
                email = request.POST.get('email')
                mobile = request.POST.get('mobile')
                address = request.POST.get('address')
                form.save()
            return redirect('dashboard', section='home')
        else:
            details = Member.objects.get(username=request.user.username)
            return render(request, 'product/editprofile.html', {'details': details})
    elif section == 'orders':
        return render(request, 'product/dashboard.html')
    elif section == 'coins':
         user = Member.objects.get(username=request.user.username)
         coins_history = Transaction.objects.filter(user=user)
         return render(request, 'product/coin_history.html',{'coins_history': coins_history})
    else:
        html = '<p>Content not found.</p>'


@login_required
@permission_required('order.add_order', raise_exception=True)
def checkout(request):
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None

    cart_items = CartItem.objects.filter(user=member)
    item_totals = [(item, item.product.price * item.quantity) for item in cart_items]
    total_cost = sum(total for item, total in item_totals)
    success_message = None
    a=member.coin_balance
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
            'a': a,
    })
