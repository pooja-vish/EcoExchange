from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib import messages
from product.models import Product
from product_crud.forms import ProductForm
from user_details.models import Member
from django.utils.text import Truncator

@login_required
@permission_required('product.add_product', raise_exception=True)
def product_details(request):
    form = ProductForm()
    if request.method == 'POST':
        member = Member.objects.get(username=request.user)
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['product_name']
            description = form.cleaned_data['product_description']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            category = form.cleaned_data['category']
            image = form.cleaned_data['image']
            new_product =  Product(
                product_name=name,
                product_description=description,
                quantity=quantity,
                price=price,
                category=category,
                user=member,
                image=image
            )
            new_product.save()
            messages.success(request, 'Product added successfully!')
            form = ProductForm()
        else:
            messages.error(request, 'Error adding product.')
    else:
        form = ProductForm()
    products = Product.objects.filter(user=request.user)
    for product in products:
        product.short_description = Truncator(product.product_description).chars(125)
    categories = Product.objects.values_list('category', flat=True).distinct()
    return render(request, 'products_crud/products_crud.html', {'form': form, 'products': products, 'categories': categories})


@login_required
@permission_required('product.delete_product', raise_exception=True)
def product_delete(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    return redirect('product_details')


@login_required
@permission_required('product.change_product', raise_exception=True)
def product_update(request):
    if request.method == 'POST':
        id = request.POST.get('product_id')
        name = request.POST.get('product_name')
        description = request.POST.get('product_description')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        new_product = Product.objects.get(pk=id)
        new_product.product_name = name
        new_product.product_description = description
        new_product.image = image
        new_product.category = category
        new_product.price = price
        new_product.quantity = quantity
        new_product.save()
        messages.success(request, 'Product updated successfully!')
    return redirect('product_details')
