from django.db import models

from user_details.models import Member

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('PAPER', 'Paper'),
        ('PLASTIC', 'Plastic'),
        ('GLASS', 'Glass'),
        ('METAL', 'Metal'),
        ('ELECTRONICS', 'Electronics'),
        ('ORGANIC', 'Organic'),
        ('TEXTILES', 'Textiles'),
        ('BATTERIES', 'Batteries'),
        ('WOOD', 'Wood'),
        ('RUBBER', 'Rubber'),
        ('MIXED_MATERIALS', 'Mixed Materials'),
    ]

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    image = models.ImageField(upload_to='img/')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)


    def __str__(self):
        return self.product_name


class CartItem(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} for {self.user.username}"

    def get_total_price(self):
        return self.quantity * self.product.price

