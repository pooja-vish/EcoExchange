from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Member(User):
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    mobile_no = PhoneNumberField(null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    coin_balance = models.IntegerField(default=0)


class Transaction(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class UserHistory(models.Model):
    user_hist_id = models.IntegerField(unique=True, primary_key=True)
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    no_of_logins = models.IntegerField(default=1)
    browser_info = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=50)
    device_info = models.CharField(max_length=200)
    login_choices = [(1, 'Success'), (2, 'Failure')]
    login_status = models.IntegerField(choices=login_choices, default=2)
    login_time = models.DateTimeField(auto_now_add=True)
