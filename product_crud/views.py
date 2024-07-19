from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product
from product_crud.forms import ProductForm

def product_details(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
        img = request.FILES.get('image')
        category = request.POST.get('category')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        new_product = Product.objects.get(pk=id)
        new_product.product_name = name
        new_product.product_description = description
        new_product.img = img
        new_product.category = category
        new_product.price = price
        new_product.quantity = quantity
        new_product.save()
    return redirect('product_details')