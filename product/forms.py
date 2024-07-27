from django import forms
from .models import Auction, Member, Product

from django import forms
from .models import Auction, Member


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['product', 'current_bid', 'start_time', 'end_time']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'current_bid': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['product'].queryset = Product.objects.filter(user=user)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'mobile_no', 'address']
