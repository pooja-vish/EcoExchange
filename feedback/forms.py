from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter your title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Please enter the details'}),
        }
