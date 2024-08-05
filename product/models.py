from django.db import models
from user_details.models import Member
from django.core.validators import MinValueValidator

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
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.IntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class Queries(models.Model):
    SUPPORT_CHOICES = [
        ('Account_Management', 'Account Management'),
        ('Technical_issues', 'Technical issues'),
        ('Billing_payments', 'Billing & Payments'),
        ('Product_service', 'Product Service Information'),
        ('Other', 'Other')
    ]
    choices = models.CharField(max_length=50, choices=SUPPORT_CHOICES)
    description = models.TextField()
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    ticket_id = models.IntegerField(primary_key=True, null=False, blank=False)
class Auction(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_winner = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Auction for {self.product.product_name}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.auction.product.product_name}"


class CartItem(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='cart')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} for {self.user.username}"

    def get_total_price(self):
        return self.quantity * self.product.price
