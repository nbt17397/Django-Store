
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m', default=None)


class ItemBase(models.Model):
    class Meta:
        abstract = True
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class Customer(ItemBase):
    class Meta:
        unique_together = ['customer_name', 'contact_name']
    customer_name = models.CharField(max_length=100, null=False)
    contact_name = models.CharField(max_length=100, null=False)
    address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    postalCode = models.TextField(null=True, blank=True)
    country = models.CharField(null=True, max_length=30)

    def __str__(self) -> str:
        return self.customer_name


class Employee(ItemBase):

    class Meta:
        unique_together = ['last_name', 'first_name']

    last_name = models.CharField(max_length=50, null=False)
    first_name = models.CharField(max_length=50, null=False)
    birth_day = models.DateTimeField()
    photo = models.ImageField(upload_to='uploads/%Y/%m', default=None)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.last_name


class Category(ItemBase):

    category_name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.category_name


class Supplier(ItemBase):

    supplier_name = models.CharField(max_length=200, null=False)
    contact_name = models.CharField(max_length=200, null=False)
    address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    postalCode = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.supplier_name


class Shipper(ItemBase):
    unique_together = ['shipper_name', 'phone']

    shipper_name = models.CharField(max_length=200, null=False)
    phone = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.shipper_name


class Product(ItemBase):
    class Meta:
        unique_together = ['product_name', 'category']

    product_name = models.CharField(max_length=200, null=False)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False)
    unit = models.CharField(max_length=200, null=False)
    price = models.FloatField(null=False)

    def __str__(self) -> str:
        return self.product_name


class Order(ItemBase):

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)


class OrderDetail(ItemBase):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False)
