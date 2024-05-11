from django.contrib import admin
from . models import MyUser, Product, Order, OrderItem

admin.site.register(MyUser)

admin.site.register(Product)

admin.site.register(Order)

admin.site.register(OrderItem)

