from django.contrib import admin
from .models import CustomUser, Purchase
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Purchase)