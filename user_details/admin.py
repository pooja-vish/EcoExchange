from django.contrib import admin
from .models import Member, UserHistory, Transaction

# Register your models here.
#admin.site.register(Member)
admin.site.register(UserHistory)
admin.site.register(Transaction)

@admin.register(Member)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'mobile_no', 'country', 'coin_balance')

