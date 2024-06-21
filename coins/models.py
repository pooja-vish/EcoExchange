from django.db import models

# Create your models here.
class Coins(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to User model
    unused_coins = models.IntegerField(default=0)
    used_coins = models.IntegerField(default=0)
    expired_coins = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.unused_coins} Coins'
