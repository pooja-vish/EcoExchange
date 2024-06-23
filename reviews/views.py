# Example views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Review
from .forms import ReviewForm


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product_id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_id = product_id
            review.user_id = request.user.id  # Assuming you have user authentication
            review.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'product_detail.html', context)
