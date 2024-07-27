from django.urls import path
from .views import feedback, feedback_thank_you_view

urlpatterns = [
    path('feedback/', feedback, name='feedback'),  # Home page of css
    path('thank-you/', feedback_thank_you_view, name='thank_you'),
]
