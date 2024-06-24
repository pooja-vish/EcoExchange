from django.db import models
from user_details.models import Member
# Create your models here.
class Order(models.Model):
    order_id = models.AutoField(primary_key=True),
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE),
    order_date = models.DateField(auto_now_add=True),
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.order_id)

class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True),
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE),
    #product_id = models.ForeignKey(Product, on_delete=models.CASCADE),
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.order_item_id)


