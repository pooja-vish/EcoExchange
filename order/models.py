from django.db import models
from django.utils import timezone
from user_details.models import Member
from product.models import Product


# Create your models here.
'''class Order(models.Model):
    order_id = models.AutoField(primary_key=True),
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE),
    order_date = models.DateField(auto_now_add=True),
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.order_id)'''

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    order_date = models.DateField(default=timezone.now)
    order_amount = models.IntegerField()
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES, default='P')

    def __str__(self):
        return f"Order {self.order_id} - {self.get_order_status_display()}"

class OrderItem(models.Model):
    #order_item_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.order_id)
