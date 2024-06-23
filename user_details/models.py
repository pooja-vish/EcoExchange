from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Member(User):
    user_id = models.IntegerField(unique=True, primary_key=True)
    address = models.TextField()
    city=models.CharField(default='Windsor', max_length=200)
    mobile_no=PhoneNumberField(unique=True)
    country=models.CharField(default='Canada', max_length=200)

class UserHistory(models.Model):
    user_hist_id = models.IntegerField(unique=True, primary_key=True)
    user_id =models.ForeignKey(Member, on_delete=models.CASCADE)
    no_of_logins=models.IntegerField(default=1)
    browser_info = models.CharField(max_length=200)
    ip_address=models.CharField(max_length=50)
    device_info=models.CharField(max_length=200)
    login_choices =[(1, 'Success'), (2, 'Failure')]
    login_status=models.IntegerField(choices=login_choices, default=2)
    login_time=models.DateTimeField(auto_now_add=True)
