from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Customer, LineItem, Order, Product

# Register your models here.

admin.site.register(Customer)
admin.site.register(LineItem)
admin.site.register(Order)
admin.site.register(Product)
