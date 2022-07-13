from django.contrib import admin
from .models import Category, Customer, Employee, Order, OrderDetail, Product, Shipper, Supplier, User

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Employee)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Shipper)
admin.site.register(Product)
admin.site.register(Supplier)
