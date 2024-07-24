from django.contrib import admin
from .models import Product, CartItem, Auction, Bid

admin.site.register(Product)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(CartItem)
# Register your models here.
