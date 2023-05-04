from django.contrib import admin

from core.models import Customer, Seller, Order, Item

# Register your models here.
admin.site.register((Item, Order, Seller, Customer))
