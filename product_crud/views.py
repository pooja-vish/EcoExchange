from django.shortcuts import render, redirect
from product.models import Product
from product_crud.forms import ProductForm


def product_details(request):
    print(request.method)
    form=ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form.is_valid()
        name = form.cleaned_data['product_name']
        description = form.cleaned_data['product_description']
        quantity = form.cleaned_data['quantity']
        price = form.cleaned_data['price']
        category = form.cleaned_data['category']
        user = form.cleaned_data['user']
        image = form.cleaned_data['image']
        new_product = Product(product_name=name, product_description=description, quantity=quantity, price=price, category=category, user=user, image=image)
        new_product.save()
        form = ProductForm()
    else:
        form = ProductForm()
    products = Product.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct()
    return render(request, 'products_crud/products_crud.html', {'form': form, 'products': products, 'categories': categories})

def product_delete(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        product.delete()
    return redirect('product_details')

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
    return redirect('product_details')