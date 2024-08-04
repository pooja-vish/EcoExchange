from django.contrib import admin
from .models import Product, CartItem, Auction, Bid, Queries

admin.site.register(Product)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(CartItem)
admin.site.register(Queries)
# Register your models here.
