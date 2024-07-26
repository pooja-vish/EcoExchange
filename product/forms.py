from django import forms
from .models import Auction, Member


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['product', 'current_bid', 'start_time', 'end_time']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'mobile_no', 'address']
