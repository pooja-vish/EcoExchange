from django.contrib import admin
from .models import Review  # Use relative import within the app

admin.site.register(Review)
